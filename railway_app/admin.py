from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.utils.html import format_html
from .models import Station, Train, Route, Schedule, Booking, BookingLeg, UserProfile, AdminSettings

# ==================== Station Admin ====================
@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'city', 'state', 'created_at')
    list_filter = ('city', 'state', 'created_at')
    search_fields = ('code', 'name', 'city')
    ordering = ('name',)
    
    fieldsets = (
        ('Station Information', {
            'fields': ('code', 'name', 'city', 'state')
        }),
        ('Location', {
            'fields': ('latitude', 'longitude'),
            'classes': ('collapse',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('code', 'created_at')
        return ()

# ==================== Train Admin ====================
@admin.register(Train)
class TrainAdmin(admin.ModelAdmin):
    list_display = ('train_number', 'train_name', 'train_type', 'total_capacity', 'is_active', 'status_badge')
    list_filter = ('train_type', 'is_active', 'created_at')
    search_fields = ('train_number', 'train_name')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('train_number', 'train_name', 'train_type', 'operator', 'is_active')
        }),
        ('Coach Configuration', {
            'fields': ('total_coaches', 'seats_per_coach')
        }),
        ('Seat Class Distribution', {
            'fields': ('ac_first_seats', 'ac_two_tier_seats', 'ac_three_tier_seats', 
                      'sleeper_seats', 'general_seats')
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    def status_badge(self, obj):
        color = 'green' if obj.is_active else 'red'
        status = 'Active' if obj.is_active else 'Inactive'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            status
        )
    status_badge.short_description = 'Status'

# ==================== Route Admin ====================
@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('train', 'source', 'destination', 'distance', 'calculated_fare', 'is_active')
    list_filter = ('train', 'source', 'destination', 'is_active')
    search_fields = ('train__train_number', 'source__name', 'destination__name')
    
    fieldsets = (
        ('Route Information', {
            'fields': ('train', 'source', 'destination', 'is_active')
        }),
        ('Distance & Duration', {
            'fields': ('distance', 'duration_hours', 'duration_minutes')
        }),
        ('Pricing', {
            'fields': ('base_fare_per_km',)
        }),
    )
    
    readonly_fields = ('created_at',)

# ==================== Schedule Admin ====================
@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('route', 'departure_time', 'arrival_time', 'runs_on_display', 'total_available', 'is_active')
    list_filter = ('route__train', 'is_active', 'departure_time')
    search_fields = ('route__train__train_number', 'route__source__name')
    
    fieldsets = (
        ('Schedule Information', {
            'fields': ('route', 'departure_time', 'arrival_time', 'runs_on', 'is_active')
        }),
        ('Seat Availability', {
            'fields': ('ac_first_available', 'ac_two_tier_available', 'ac_three_tier_available',
                      'sleeper_available', 'general_available'),
            'classes': ('wide',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    def total_available(self, obj):
        total = (obj.ac_first_available + obj.ac_two_tier_available + 
                obj.ac_three_tier_available + obj.sleeper_available + obj.general_available)
        return f"{total} seats"
    total_available.short_description = 'Total Available'
    
    def runs_on_display(self, obj):
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        running_days = [days[int(d)] for d in obj.runs_on if d.isdigit() and int(d) < 7]
        return ', '.join(running_days) if running_days else 'N/A'
    runs_on_display.short_description = 'Runs On'

# ==================== Booking Admin ====================
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('pnr', 'passenger_name', 'journey_date', 'status_badge', 'total_fare', 'booking_date')
    list_filter = ('status', 'journey_date', 'seat_class', 'booking_date')
    search_fields = ('pnr', 'passenger_name', 'passenger_email', 'passenger_phone')
    readonly_fields = ('pnr', 'booking_date', 'cancellation_date')
    
    fieldsets = (
        ('Booking Information', {
            'fields': ('pnr', 'user', 'booking_date', 'status', 'journey_date')
        }),
        ('Passenger Details', {
            'fields': ('passenger_name', 'passenger_email', 'passenger_phone', 
                      'passenger_age', 'passenger_gender')
        }),
        ('Booking Details', {
            'fields': ('seat_class', 'total_fare', 'is_refundable')
        }),
        ('Cancellation', {
            'fields': ('cancellation_date', 'refund_amount'),
            'classes': ('collapse',)
        }),
    )
    
    def status_badge(self, obj):
        colors = {
            'CONFIRMED': 'green',
            'PENDING': 'orange',
            'CANCELLED': 'red'
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def has_add_permission(self, request):
        return False  # Bookings created through app, not admin

# ==================== Booking Leg Admin ====================
@admin.register(BookingLeg)
class BookingLegAdmin(admin.ModelAdmin):
    list_display = ('booking', 'route', 'leg_sequence', 'seat_number', 'leg_fare')
    list_filter = ('route__train', 'leg_sequence')
    search_fields = ('booking__pnr', 'seat_number')
    readonly_fields = ('created_at',)
    
    def has_add_permission(self, request):
        return False  # Created through booking

# ==================== User Profile Admin ====================
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'city', 'total_bookings', 'total_spent', 'is_verified')
    list_filter = ('is_verified', 'city', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone')
    readonly_fields = ('total_bookings', 'total_spent', 'created_at')

# ==================== Admin Settings ====================
@admin.register(AdminSettings)
class AdminSettingsAdmin(admin.ModelAdmin):
    list_display = ('key', 'value', 'updated_at')
    search_fields = ('key', 'description')
    
    fieldsets = (
        ('Setting', {
            'fields': ('key', 'value', 'description')
        }),
    )
    
    readonly_fields = ('updated_at',)