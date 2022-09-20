from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Passenger, Trip
from .serializers import PassengerSerializer, TripSerializer
from .tasks import cal_distance, cal_distance_update
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework import status


@api_view(['GET'])
def ApiOverview(request):
    api_urls = {
        'all_passengers': '/passengers',
        'all_trips': '/trips',
        'Add Passenger': '/create-pass',
        'Add Trip': '/create-trip',
        'Update Passenger': '/update-pass/pk',
        'Update Trip': '/update-trip/pk',
        'Delete Passenger': '/p/pk/delete',
        'Delete Trip': '/t/pk/delete'
    }
  
    return Response(api_urls)



@api_view(['POST'])
def add_passengers(request):
    pas = PassengerSerializer(data=request.data)
  
    # validating for already existing data
    if Passenger.objects.filter(**request.data).exists():
        raise serializers.ValidationError('This data already exists')
  
    if pas.is_valid():
        pas.save()
        return Response(pas.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def add_trips(request):
    trip = TripSerializer(data=request.data)
  
    # validating for already existing data
    if Trip.objects.filter(**request.data).exists():
        raise serializers.ValidationError('This data already exists')
  
    if trip.is_valid():
        # go to celery
        cal_distance.delay(trip.data)
        
        return Response(trip.data)
        
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def view_passengers(request):
    # checking for the parameters from the URL
    if request.query_params:
        items = Passenger.objects.filter(**request.query_params.dict())
    else:
        items = Passenger.objects.all()
    
    serializer = PassengerSerializer(items, many=True)

    # if there is something in items else raise error
    if items:
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def view_trips(request):
	# checking for the parameters from the URL
    if request.query_params:
        items = Trip.objects.filter(**request.query_params.dict())
    else:
        items = Trip.objects.all()
    serializer = TripSerializer(items, many=True)

    # if there is something in items else raise error
    if items:
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def update_passenger(request, pk):
    item = Passenger.objects.get(pk=pk)
    data = PassengerSerializer(instance=item, data=request.data)
  
    if data.is_valid():
        data.save()
        return Response(data.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def update_trip(request, pk):
    # celery
    cal_distance_update.delay(pk, request.data)

    item = Trip.objects.get(pk=pk)
    data = TripSerializer(instance=item, data=request.data)
  
    if data.is_valid():
        return Response(request.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def delete_passengers(request, pk):
    item = get_object_or_404(Passenger, pk=pk)
    item.delete()
    return Response(status=status.HTTP_202_ACCEPTED)

@api_view(['DELETE'])
def delete_trips(request, pk):
    item = get_object_or_404(Trip, pk=pk)
    item.delete()
    return Response(status=status.HTTP_202_ACCEPTED)