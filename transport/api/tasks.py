from transport.celery import app
from .models import Trip
import math
from .serializers import TripSerializer
from rest_framework import status

@app.task(bind=True)
def cal_distance(self, data):
    """Perform a calculation & update the status"""
    p1 = data["start_point"]
    p2 = data["end_point"]

    x1, y1 = p1.split(",")
    x2, y2 = p2.split(",")

    p = [int(x1), int(y1)]
    q = [int(x2), int(y2)]

    d = math.dist(p, q)

    data["total_distance"] = d

    trip = TripSerializer(data=data)
    
    if trip.is_valid():
        trip.save()
    else:
        print(trip.errors)
    


@app.task(bind=True)
def cal_distance_update(self, pk, data):
    """Perform a calculation & update the status"""
    i = Trip.objects.get(pk=pk)
    p1 = data["start_point"]
    p2 = data["end_point"]

    x1, y1 = p1.split(",")
    x2, y2 = p2.split(",")

    p = [int(x1), int(y1)]
    q = [int(x2), int(y2)]

    d = math.dist(p, q)

    data["total_distance"] = d

    trip = TripSerializer(instance=i, data=data)
    
    if trip.is_valid():
        trip.save()
    
