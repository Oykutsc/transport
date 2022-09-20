from django.db.models import fields
from rest_framework import serializers
from .models import Passenger, Trip
  
class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = ('id', 'name', 'surname', 'email', 'home')

class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = ('id', 'passenger_id', 'start_time', 'start_point', 'end_point', 'total_distance')