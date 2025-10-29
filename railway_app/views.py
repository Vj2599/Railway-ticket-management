from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, FileResponse, HttpResponse
from django.views.decorators.http import require_http_methods, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Q, Sum, Count
from django.utils import timezone
from django.core.mail import send_mail
from datetime import datetime, timedelta
import json, uuid
from decimal import Decimal
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from io import BytesIO

from .models import Station, Train, Route, Schedule, Booking, BookingLeg, UserProfile

# ==================== HELPER FUNCTIONS ====================

def find_direct_trains(source_station, dest_station, journey_date, seat_class):
    """Find direct trains with available seats"""
    weekday = journey_date.weekday()
    
    routes = Route.objects.filter(
        source=source_station,
        destination=dest_station,
        is_active=True
    )
    
    direct_options = []
    
    for route in routes:
        schedules = Schedule.objects.filter(
            route=route,
            is_active=True
        ).exclude(runs_on__exact='')
        
        for schedule in schedules:
            if str(weekday) not in schedule.runs_on:
                continue
            
            available = schedule.get_available_seats(seat_class)
            if available > 0:
                direct_options.append({
                    'type': 'direct',
                    'schedule': schedule,
                    'route': route,
                    'available_seats': available,
                    'fare': Decimal(str(route.calculated_fare)),
                    'duration': f"{route.duration_hours}h {route.duration_minutes}m",
                })
    
    return direct_options

def find_connecting_trains(source_station, dest_station, journey_date, seat_class, min_buffer=30):
    """Find 2-leg connecting routes with optimal second leg selection based on earliest arrival"""
    weekday = journey_date.weekday()
    connecting_options = []

    # Find all intermediate stations
    intermediate_routes = Route.objects.filter(
        source=source_station,
        is_active=True
    ).exclude(destination=dest_station)

    for first_leg_route in intermediate_routes:
        intermediate_station = first_leg_route.destination

        # Find second leg routes
        second_leg_routes = Route.objects.filter(
            source=intermediate_station,
            destination=dest_station,
            is_active=True
        )

        first_schedules = Schedule.objects.filter(
            route=first_leg_route,
            is_active=True
        ).exclude(runs_on__exact='')

        for first_schedule in first_schedules:
            if str(weekday) not in first_schedule.runs_on:
                continue

            first_available = first_schedule.get_available_seats(seat_class)
            if first_available == 0:
                continue

            # For this first leg, find the best second leg (earliest arrival at destination)
            best_second_leg = None
            earliest_arrival = None

            for second_leg_route in second_leg_routes:
                second_schedules = Schedule.objects.filter(
                    route=second_leg_route,
                    is_active=True
                ).exclude(runs_on__exact='')

                for second_schedule in second_schedules:
                    if str(weekday) not in second_schedule.runs_on:
                        continue

                    second_available = second_schedule.get_available_seats(seat_class)
                    if second_available == 0:
                        continue

                    # Calculate connection timing
                    first_arrival = datetime.combine(journey_date, first_schedule.arrival_time)
                    second_departure = datetime.combine(journey_date, second_schedule.departure_time)

                    if second_departure <= first_arrival:
                        second_departure += timedelta(days=1)

                    buffer_minutes = (second_departure - first_arrival).total_seconds() / 60

                    if buffer_minutes >= min_buffer:
                        # Calculate total arrival time at destination
                        second_arrival = datetime.combine(journey_date, second_schedule.arrival_time)
                        if second_arrival <= second_departure:
                            second_arrival += timedelta(days=1)

                        # Check if this is the earliest arrival
                        if earliest_arrival is None or second_arrival < earliest_arrival:
                            earliest_arrival = second_arrival
                            best_second_leg = {
                                'schedule': second_schedule,
                                'route': second_leg_route,
                                'available_seats': second_available,
                                'buffer_minutes': int(buffer_minutes),
                                'arrival_time': second_arrival,
                            }

            # If we found a valid second leg, add the connecting option
            if best_second_leg:
                total_fare = Decimal(str(first_leg_route.calculated_fare + best_second_leg['route'].calculated_fare))

                connecting_options.append({
                    'type': 'connecting',
                    'leg_1': {
                        'schedule': first_schedule,
                        'route': first_leg_route,
                        'available_seats': first_available,
                    },
                    'leg_2': {
                        'schedule': best_second_leg['schedule'],
                        'route': best_second_leg['route'],
                        'available_seats': best_second_leg['available_seats'],
                    },
                    'buffer_minutes': best_second_leg['buffer_minutes'],
                    'total_fare': total_fare,
                    'total_distance': first_leg_route.distance + best_second_leg['route'].distance,
                    'total_arrival_time': best_second_leg['arrival_time'],
                })

    # Sort connecting options by earliest total arrival time
    connecting_options.sort(key=lambda x: x['total_arrival_time'])

    return connecting_options

def generate_ticket_pdf(booking):
    """Generate PDF ticket"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Title
    title = Paragraph("<b>RAILWAY E-TICKET</b>", styles['Heading1'])
    story.append(title)
    story.append(Spacer(1, 0.2*inch))
    
    # PNR Info
    pnr_data = [
        ['PNR:', booking.pnr, 'Status:', booking.get_status_display()],
        ['Booking Date:', booking.booking_date.strftime('%d-%m-%Y'), 
         'Journey Date:', booking.journey_date.strftime('%d-%m-%Y')],
    ]
    story.append(Table(pnr_data, colWidths=[1.5*inch, 2*inch, 1.5*inch, 2*inch]))
    story.append(Spacer(1, 0.2*inch))
    
    # Passenger Info
    story.append(Paragraph("<b>Passenger Details</b>", styles['Heading3']))
    pass_data = [
        ['Name:', booking.passenger_name],
        ['Age/Gender:', f"{booking.passenger_age} / {booking.get_passenger_gender_display()}"],
        ['Email:', booking.passenger_email],
    ]
    story.append(Table(pass_data, colWidths=[1.5*inch, 4*inch]))
    story.append(Spacer(1, 0.2*inch))
    
    # Journey Details
    story.append(Paragraph("<b>Journey Details</b>", styles['Heading3']))
    journey_data = [['Train', 'From', 'To', 'Depart', 'Arrive', 'Class', 'Seat', 'Fare']]
    
    for leg in booking.legs.all():
        journey_data.append([
            leg.route.train.train_number,
            leg.route.source.code,
            leg.route.destination.code,
            leg.schedule.departure_time.strftime('%H:%M'),
            leg.schedule.arrival_time.strftime('%H:%M'),
            booking.get_seat_class_display(),
            leg.seat_number,
            f"₹{leg.leg_fare}"
        ])
    
    story.append(Table(journey_data, colWidths=[1*inch]*8))
    story.append(Spacer(1, 0.2*inch))
    
    # Total Fare
    story.append(Paragraph(f"<b>Total Fare: ₹{booking.total_fare}</b>", styles['Heading2']))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

# ==================== PASSENGER VIEWS ====================

def home(request):
    """Home page with search form"""
    stations = Station.objects.all().order_by('name')
    context = {'stations': stations}
    return render(request, 'home.html', context)

@require_http_methods(["GET", "POST"])
def search_trains(request):
    """AJAX endpoint for train search"""
    if request.method == 'POST':
        data = json.loads(request.body)

        source_id = data.get('source_id')
        dest_id = data.get('destination_id')
        journey_date_str = data.get('journey_date')
        seat_class = data.get('seat_class', 'SLEEPER')

        try:
            source = Station.objects.get(id=source_id)
            destination = Station.objects.get(id=dest_id)
            journey_date = datetime.strptime(journey_date_str, '%Y-%m-%d').date()

            # Check if date is in future
            if journey_date < timezone.now().date():
                return JsonResponse({
                    'error': 'Journey date cannot be in the past',
                    'status': 'error'
                })

            # Find direct trains
            direct = find_direct_trains(source, destination, journey_date, seat_class)

            # Find connecting trains - only for authenticated users
            connecting = []
            if request.user.is_authenticated:
                connecting = find_connecting_trains(source, destination, journey_date, seat_class)
            
            # Serialize response
            direct_serialized = []
            for train in direct:
                direct_serialized.append({
                    'id': train['schedule'].id,
                    'train_number': train['route'].train.train_number,
                    'train_name': train['route'].train.train_name,
                    'from': train['route'].source.code,
                    'to': train['route'].destination.code,
                    'departure': str(train['schedule'].departure_time),
                    'arrival': str(train['schedule'].arrival_time),
                    'duration': train['duration'],
                    'distance': train['route'].distance,
                    'available_seats': train['available_seats'],
                    'fare': float(train['fare']),
                    'schedule_id': train['schedule'].id,
                    'route_id': train['route'].id,
                })
            
            connecting_serialized = []
            for conn in connecting:
                connecting_serialized.append({
                    'leg_1_schedule': conn['leg_1']['schedule'].id,
                    'leg_1_train': conn['leg_1']['route'].train.train_number,
                    'leg_1_from': conn['leg_1']['route'].source.code,
                    'leg_1_to': conn['leg_1']['route'].destination.code,
                    'leg_1_departure': str(conn['leg_1']['schedule'].departure_time),
                    'leg_1_arrival': str(conn['leg_1']['schedule'].arrival_time),
                    'leg_1_available': conn['leg_1']['available_seats'],
                    
                    'leg_2_schedule': conn['leg_2']['schedule'].id,
                    'leg_2_train': conn['leg_2']['route'].train.train_number,
                    'leg_2_from': conn['leg_2']['route'].source.code,
                    'leg_2_to': conn['leg_2']['route'].destination.code,
                    'leg_2_departure': str(conn['leg_2']['schedule'].departure_time),
                    'leg_2_arrival': str(conn['leg_2']['schedule'].arrival_time),
                    'leg_2_available': conn['leg_2']['available_seats'],
                    
                    'buffer_minutes': conn['buffer_minutes'],
                    'total_fare': float(conn['total_fare']),
                    'total_distance': conn['total_distance'],
                })
            
            return JsonResponse({
                'status': 'success',
                'direct_count': len(direct),
                'connecting_count': len(connecting),
                'direct_trains': direct_serialized,
                'connecting_trains': connecting_serialized,
            })
        
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'error': str(e)
            })

@require_http_methods(["GET", "POST"])
def booking(request):
    """Booking page"""
    if request.method == 'GET':
        schedule_id = request.GET.get('schedule_id')
        route_id = request.GET.get('route_id')
        leg_2_schedule_id = request.GET.get('leg_2_schedule_id')
        seat_class = request.GET.get('seat_class', 'SLEEPER')
        
        # Fetch schedule and route
        schedule = get_object_or_404(Schedule, id=schedule_id)
        route = get_object_or_404(Route, id=route_id)
        
        schedules = [schedule]
        routes = [route]
        total_fare = route.calculated_fare
        is_connecting = False
        
        if leg_2_schedule_id:
            leg_2_schedule = get_object_or_404(Schedule, id=leg_2_schedule_id)
            leg_2_route = leg_2_schedule.route
            schedules.append(leg_2_schedule)
            routes.append(leg_2_route)
            total_fare += leg_2_route.calculated_fare
            is_connecting = True
        
        context = {
            'schedules': schedules,
            'routes': routes,
            'seat_class': seat_class,
            'total_fare': total_fare,
            'is_connecting': is_connecting,
        }
        return render(request, 'booking.html', context)
    
    elif request.method == 'POST':
        data = json.loads(request.body)
        
        passenger_name = data.get('passenger_name')
        passenger_email = data.get('passenger_email')
        passenger_phone = data.get('passenger_phone')
        passenger_age = int(data.get('passenger_age'))
        passenger_gender = data.get('passenger_gender')
        seat_class = data.get('seat_class')
        journey_date = data.get('journey_date')
        schedule_ids = data.get('schedule_ids', [])
        seat_numbers = data.get('seat_numbers', [])
        total_fare = Decimal(str(data.get('total_fare')))
        
        try:
            # Create booking
            booking_obj = Booking.objects.create(
                passenger_name=passenger_name,
                passenger_email=passenger_email,
                passenger_phone=passenger_phone,
                passenger_age=passenger_age,
                passenger_gender=passenger_gender,
                seat_class=seat_class,
                journey_date=journey_date,
                total_fare=total_fare,
                status='CONFIRMED'
            )
            
            # Create booking legs and reduce seat availability
            for idx, schedule_id in enumerate(schedule_ids):
                schedule = Schedule.objects.get(id=schedule_id)
                route = schedule.route
                
                # Create booking leg
                BookingLeg.objects.create(
                    booking=booking_obj,
                    schedule=schedule,
                    route=route,
                    seat_number=seat_numbers[idx],
                    leg_fare=Decimal(str(route.calculated_fare)),
                    leg_sequence=idx + 1
                )
                
                # Reduce available seats
                schedule.reduce_available_seats(seat_class)
            
            # Send confirmation email
            send_booking_confirmation(booking_obj)
            
            return JsonResponse({
                'status': 'success',
                'pnr': booking_obj.pnr,
                'message': 'Booking confirmed successfully!'
            })
        
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'error': str(e)
            })

def send_booking_confirmation(booking):
    """Send booking confirmation email"""
    subject = f"Booking Confirmed - PNR: {booking.pnr}"
    message = f"""
Dear {booking.passenger_name},

Your ticket has been successfully booked!

PNR: {booking.pnr}
Journey Date: {booking.journey_date}
Seat Class: {booking.get_seat_class_display()}
Total Fare: ₹{booking.total_fare}

Please keep your PNR for future reference.

Best regards,
Railway Ticket Management
    """
    
    try:
        send_mail(subject, message, 'noreply@railway.com', [booking.passenger_email])
    except:
        pass

def confirmation(request):
    """Confirmation page"""
    pnr = request.GET.get('pnr')
    booking = get_object_or_404(Booking, pnr=pnr)
    context = {'booking': booking}
    return render(request, 'confirmation.html', context)

def search_results(request):
    """Search results page"""
    return render(request, 'search_results.html')

@login_required
def my_bookings(request):
    """User's bookings page"""
    bookings = Booking.objects.filter(user=request.user)
    context = {'bookings': bookings}
    return render(request, 'my_bookings.html', context)

@login_required
def cancel_booking(request, pnr):
    """Cancel booking"""
    booking = get_object_or_404(Booking, pnr=pnr)
    
    if request.user != booking.user and not request.user.is_staff:
        return redirect('home')
    
    if request.method == 'POST':
        if booking.status == 'CONFIRMED':
            booking.status = 'CANCELLED'
            booking.cancellation_date = timezone.now()
            booking.refund_amount = booking.total_fare * Decimal('0.9')  # 90% refund
            booking.save()
            
            # Restore seat availability
            for leg in booking.legs.all():
                leg.schedule.available_seats += 1
                leg.schedule.save()
        
        return redirect('my_bookings')
    
    context = {'booking': booking}
    return render(request, 'cancel_booking.html', context)

@require_http_methods(["GET"])
def download_ticket(request, pnr):
    """Download ticket as PDF"""
    booking = get_object_or_404(Booking, pnr=pnr)
    
    pdf_buffer = generate_ticket_pdf(booking)
    response = FileResponse(pdf_buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="ticket_{pnr}.pdf"'
    return response

@require_http_methods(["GET"])
def station_autocomplete(request):
    """AJAX autocomplete for stations"""
    query = request.GET.get('q', '')
    stations = Station.objects.filter(
        Q(name__icontains=query) | Q(code__icontains=query)
    )[:10]
    
    data = [{'id': s.id, 'text': f"{s.code} - {s.name}"} for s in stations]
    return JsonResponse(data, safe=False)

# ==================== AUTH VIEWS ====================

def register(request):
    """User registration"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        if password != password2:
            return render(request, 'auth/register.html', {'error': 'Passwords do not match'})
        
        if User.objects.filter(username=username).exists():
            return render(request, 'auth/register.html', {'error': 'Username already exists'})
        
        user = User.objects.create_user(username=username, email=email, password=password)
        UserProfile.objects.create(user=user)
        
        login(request, user)
        return redirect('home')
    
    return render(request, 'auth/register.html')

def user_login(request):
    """User login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'auth/login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'auth/login.html')

def user_logout(request):
    """User logout"""
    logout(request)
    return redirect('home')

# ==================== ADMIN VIEWS ====================

def is_admin(user):
    return user.is_staff and user.is_superuser

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    """Admin dashboard"""
    context = {
        'total_trains': Train.objects.count(),
        'total_stations': Station.objects.count(),
        'total_bookings': Booking.objects.count(),
        'confirmed_bookings': Booking.objects.filter(status='CONFIRMED').count(),
        'cancelled_bookings': Booking.objects.filter(status='CANCELLED').count(),
        'total_revenue': Booking.objects.filter(status='CONFIRMED').aggregate(Sum('total_fare'))['total_fare__sum'] or 0,
    }
    return render(request, 'admin/dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def manage_trains(request):
    """Manage trains"""
    trains = Train.objects.all()
    context = {'trains': trains}
    return render(request, 'admin/manage_trains.html', context)

@login_required
@user_passes_test(is_admin)
def manage_stations(request):
    """Manage stations"""
    stations = Station.objects.all()
    context = {'stations': stations}
    return render(request, 'admin/manage_stations.html', context)

@login_required
@user_passes_test(is_admin)
def manage_routes(request):
    """Manage routes"""
    routes = Route.objects.all()
    context = {'routes': routes}
    return render(request, 'admin/manage_routes.html', context)

@login_required
@user_passes_test(is_admin)
def manage_schedules(request):
    """Manage schedules"""
    schedules = Schedule.objects.all()
    context = {'schedules': schedules}
    return render(request, 'admin/manage_schedules.html', context)

@login_required
@user_passes_test(is_admin)
def manage_bookings(request):
    """Manage bookings"""
    bookings = Booking.objects.all()
    context = {'bookings': bookings}
    return render(request, 'admin/manage_bookings.html', context)

@login_required
@user_passes_test(is_admin)
def analytics(request):
    """Analytics page"""
    total_revenue = Booking.objects.filter(status='CONFIRMED').aggregate(Sum('total_fare'))['total_fare__sum'] or 0
    monthly_bookings = Booking.objects.filter(status='CONFIRMED').count()
    
    # Most used routes
    top_routes = Route.objects.annotate(
        booking_count=Count('bookingleg__booking')
    ).order_by('-booking_count')[:5]
    
    context = {
        'total_revenue': total_revenue,
        'monthly_bookings': monthly_bookings,
        'top_routes': top_routes,
    }
    return render(request, 'admin/analytics.html', context)