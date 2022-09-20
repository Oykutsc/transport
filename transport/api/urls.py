from django.urls import path
from . import views

urlpatterns = [
	path('', views.ApiOverview, name='home'),
    path('create-pass/', views.add_passengers, name='add-passengers'),
    path('create-trip/', views.add_trips, name='add-trips'),
    path('passengers/', views.view_passengers, name='view-passengers'),
    path('trips/', views.view_trips, name='view-trips'),
    path('update-pass/<str:pk>/', views.update_passenger, name='update-passenger'),
    path('update-trip/<str:pk>/', views.update_trip, name='update-trip'),
    path('p/<str:pk>/delete/', views.delete_passengers, name='delete-passengers'),
    path('t/<str:pk>/delete/', views.delete_trips, name='delete-trips'),
]
