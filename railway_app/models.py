from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime, timedelta
import uuid

# ==================== Station Model ====================
class Station(models.Model):
    code = models.CharField(max_length=5, unique=True, help_text="Station code (e.g., BZA)")
    name = models.CharField(max_length=100, unique=True, help_text="Full station name")
    city = models.CharField(max_length=50, help_text="City name")
    state = models.CharField(max_length=50, default="")
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = "Stations"
    
    def __str__(self):
        return f"{self.code} - {self.name} ({self.city})"

# ==================== Train Model ====================
class Train(models.Model):
    TRAIN_TYPES = [
        ('EXPRESS', 'Express'),
        ('RAPID', 'Rapid'),
        ('PASSENGER', 'Passenger'),
        ('SHATABDI', 'Shatabdi'),
        ('RAJDHANI', 'Rajdhani'),
    ]
    
    train_number = models.CharField(max_length=10, unique=True, help_text="Unique train number")
    train_name = models.CharField(max_length=100, help_text="Train name")
    train_type = models.CharField(max_length=20, choices=TRAIN_TYPES, default='EXPRESS')
    operator = models.CharField(max_length=50, default="Indian Railways")
    
    # Seat configuration
    total_coaches = models.IntegerField(default=12, validators=[MinValueValidator(1)])
    seats_per_coach = models.IntegerField(default=72, validators=[MinValueValidator(1)])
    
    # Seat class breakdown (AC First, AC 2-Tier, AC 3-Tier, Sleeper, General)
    ac_first_seats = models.IntegerField(default=0)
    ac_two_tier_seats = models.IntegerField(default=0)
    ac_three_tier_seats = models.IntegerField(default=0)
    sleeper_seats = models.IntegerField(default=0)
    general_seats = models.IntegerField(default=0)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['train_number']
        verbose_name_plural = "Trains"
    
    def __str__(self):
        return f"{self.train_number} - {self.train_name}"
    
    @property
    def total_capacity(self):
        return self.total_coaches * self.seats_per_coach

# ==================== Route Model ====================
class Route(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE, related_name='routes')
    source = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='source_routes')
    destination = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='dest_routes')
    
    distance = models.IntegerField(validators=[MinValueValidator(1)], help_text="Distance in km")
    duration_hours = models.IntegerField(default=1, validators=[MinValueValidator(0)])
    duration_minutes = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(59)])
    
    # Fare per km (will be multiplied by distance)
    base_fare_per_km = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('train', 'source', 'destination')
        ordering = ['distance']
        verbose_name_plural = "Routes"
    
    def __str__(self):
        return f"{self.train.train_number}: {self.source.code} → {self.destination.code}"
    
    @property
    def calculated_fare(self):
        return float(self.base_fare_per_km) * self.distance

# ==================== Schedule Model ====================
class Schedule(models.Model):
    WEEKDAYS = [
        (0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'),
        (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')
    ]
    
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='schedules')
    
    departure_time = models.TimeField(help_text="Departure time (HH:MM)")
    arrival_time = models.TimeField(help_text="Arrival time (HH:MM)")
    
    # Days of operation (can be multiple days)
    runs_on = models.CharField(
        max_length=7, 
        default="0123456",
        help_text="Days: 0=Mon,1=Tue,2=Wed,3=Thu,4=Fri,5=Sat,6=Sun"
    )
    
    # Seat availability by class
    ac_first_available = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    ac_two_tier_available = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    ac_three_tier_available = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    sleeper_available = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    general_available = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('route', 'departure_time')
        ordering = ['departure_time']
        verbose_name_plural = "Schedules"
    
    def __str__(self):
        return f"{self.route} @ {self.departure_time}"
    
    def get_available_seats(self, seat_class):
        """Get available seats for a specific class"""
        class_map = {
            'AC_FIRST': self.ac_first_available,
            'AC_2_TIER': self.ac_two_tier_available,
            'AC_3_TIER': self.ac_three_tier_available,
            'SLEEPER': self.sleeper_available,
            'GENERAL': self.general_available,
        }
        return class_map.get(seat_class, 0)
    
    def reduce_available_seats(self, seat_class, count=1):
        """Reduce seat count for a class"""
        class_map = {
            'AC_FIRST': 'ac_first_available',
            'AC_2_TIER': 'ac_two_tier_available',
            'AC_3_TIER': 'ac_three_tier_available',
            'SLEEPER': 'sleeper_available',
            'GENERAL': 'general_available',
        }
        attr = class_map.get(seat_class)
        if attr:
            current = getattr(self, attr, 0)
            setattr(self, attr, max(0, current - count))
            self.save()

# ==================== Booking Model ====================
class Booking(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    SEAT_CLASSES = [
        ('AC_FIRST', 'AC First Class'),
        ('AC_2_TIER', 'AC 2-Tier'),
        ('AC_3_TIER', 'AC 3-Tier'),
        ('SLEEPER', 'Sleeper'),
        ('GENERAL', 'General'),
    ]
    
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    # PNR (Passenger Name Record)
    pnr = models.CharField(max_length=10, unique=True, db_index=True, editable=False)
    
    # User reference (optional - for registered users)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings')
    
    # Passenger details
    passenger_name = models.CharField(max_length=100)
    passenger_email = models.EmailField()
    passenger_phone = models.CharField(max_length=15)
    passenger_age = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(120)])
    passenger_gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    
    # Booking details
    booking_date = models.DateTimeField(auto_now_add=True)
    journey_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    
    # Pricing
    seat_class = models.CharField(max_length=20, choices=SEAT_CLASSES)
    total_fare = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Additional info
    is_refundable = models.BooleanField(default=True)
    cancellation_date = models.DateTimeField(null=True, blank=True)
    refund_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    class Meta:
        ordering = ['-booking_date']
        verbose_name_plural = "Bookings"
    
    def __str__(self):
        return f"PNR: {self.pnr} - {self.passenger_name}"
    
    def save(self, *args, **kwargs):
        if not self.pnr:
            self.pnr = self.generate_pnr()
        super().save(*args, **kwargs)
    
    @staticmethod
    def generate_pnr():
        """Generate unique 10-character PNR"""
        return str(uuid.uuid4())[:10].upper()

# ==================== Booking Leg Model ====================
class BookingLeg(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='legs')
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    
    seat_number = models.CharField(max_length=5, help_text="e.g., 1A, 32C")
    leg_fare = models.DecimalField(max_digits=10, decimal_places=2)
    
    # For tracking connections
    leg_sequence = models.IntegerField(default=1)  # 1 for first leg, 2 for second leg, etc.
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['leg_sequence']
        verbose_name_plural = "Booking Legs"
    
    def __str__(self):
        return f"{self.booking.pnr} - Leg {self.leg_sequence}: {self.route}"

# ==================== User Profile Model ====================
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=50, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    total_bookings = models.IntegerField(default=0)
    total_spent = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

# ==================== Admin Settings Model ====================
class AdminSettings(models.Model):
    key = models.CharField(max_length=50, unique=True)
    value = models.TextField()
    description = models.CharField(max_length=200, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Admin Settings"
    
    def __str__(self):
        return f"{self.key}"
    