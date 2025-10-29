
from django import forms
from django.contrib.auth.models import User
from .models import Booking, Station, Train, Route, Schedule

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['passenger_name', 'passenger_email', 'passenger_phone', 
                  'passenger_age', 'passenger_gender', 'seat_class']
        widgets = {
            'passenger_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Full Name'
            }),
            'passenger_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email Address'
            }),
            'passenger_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number'
            }),
            'passenger_age': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Age'
            }),
            'passenger_gender': forms.Select(attrs={
                'class': 'form-control'
            }),
            'seat_class': forms.Select(attrs={
                'class': 'form-control'
            }),
        }

class StationForm(forms.ModelForm):
    class Meta:
        model = Station
        fields = ['code', 'name', 'city', 'state', 'latitude', 'longitude']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class TrainForm(forms.ModelForm):
    class Meta:
        model = Train
        fields = ['train_number', 'train_name', 'train_type', 'operator', 
                  'total_coaches', 'seats_per_coach', 'ac_first_seats', 
                  'ac_two_tier_seats', 'ac_three_tier_seats', 'sleeper_seats', 
                  'general_seats', 'is_active']
        widgets = {
            'train_number': forms.TextInput(attrs={'class': 'form-control'}),
            'train_name': forms.TextInput(attrs={'class': 'form-control'}),
            'train_type': forms.Select(attrs={'class': 'form-control'}),
            'operator': forms.TextInput(attrs={'class': 'form-control'}),
            'total_coaches': forms.NumberInput(attrs={'class': 'form-control'}),
            'seats_per_coach': forms.NumberInput(attrs={'class': 'form-control'}),
            'ac_first_seats': forms.NumberInput(attrs={'class': 'form-control'}),
            'ac_two_tier_seats': forms.NumberInput(attrs={'class': 'form-control'}),
            'ac_three_tier_seats': forms.NumberInput(attrs={'class': 'form-control'}),
            'sleeper_seats': forms.NumberInput(attrs={'class': 'form-control'}),
            'general_seats': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(),
        }

class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ['train', 'source', 'destination', 'distance', 'duration_hours', 
                  'duration_minutes', 'base_fare_per_km', 'is_active']
        widgets = {
            'train': forms.Select(attrs={'class': 'form-control'}),
            'source': forms.Select(attrs={'class': 'form-control'}),
            'destination': forms.Select(attrs={'class': 'form-control'}),
            'distance': forms.NumberInput(attrs={'class': 'form-control'}),
            'duration_hours': forms.NumberInput(attrs={'class': 'form-control'}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-control'}),
            'base_fare_per_km': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(),
        }

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['route', 'departure_time', 'arrival_time', 'runs_on', 
                  'ac_first_available', 'ac_two_tier_available', 'ac_three_tier_available',
                  'sleeper_available', 'general_available', 'is_active']
        widgets = {
            'route': forms.Select(attrs={'class': 'form-control'}),
            'departure_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'arrival_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'runs_on': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter days (e.g., 0123456 for all days)'
            }),
            'ac_first_available': forms.NumberInput(attrs={'class': 'form-control'}),
            'ac_two_tier_available': forms.NumberInput(attrs={'class': 'form-control'}),
            'ac_three_tier_available': forms.NumberInput(attrs={'class': 'form-control'}),
            'sleeper_available': forms.NumberInput(attrs={'class': 'form-control'}),
            'general_available': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(),
        }