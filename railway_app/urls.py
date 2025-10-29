
from django.urls import path
from . import views

urlpatterns = [
    # Passenger views
    path('', views.home, name='home'),
    path('search/', views.search_trains, name='search_trains'),
    path('search-results/', views.search_results, name='search_results'),
    path('booking/', views.booking, name='booking'),
    path('confirmation/', views.confirmation, name='confirmation'),
    path('download-ticket/<str:pnr>/', views.download_ticket, name='download_ticket'),

    # Autocomplete
    path('api/stations/', views.station_autocomplete, name='station_autocomplete'),

    # User views
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('cancel-booking/<str:pnr>/', views.cancel_booking, name='cancel_booking'),

    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # Admin views
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/trains/', views.manage_trains, name='manage_trains'),
    path('admin/stations/', views.manage_stations, name='manage_stations'),
    path('admin/routes/', views.manage_routes, name='manage_routes'),
    path('admin/schedules/', views.manage_schedules, name='manage_schedules'),
    path('admin/bookings/', views.manage_bookings, name='manage_bookings'),
    path('admin/analytics/', views.analytics, name='analytics'),
]
