from django.db import models
import uuid
# Create your models here.

from django.urls import reverse # Used to generate URLs by reversing the URL patterns

class Passenger(models.Model):
    """Passenger"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    name = models.CharField('Name', max_length=200)
    surname = models.CharField('Surname', max_length=200)

    email = models.EmailField('Email', max_length=200, unique=True)

    home = models.CharField('Home Location', max_length=7, help_text='Enter your home location as -,-. (Ex. 12, 45)')

    

    def __str__(self):
        """String for representing the Model object."""
        return self.id

    def get_absolute_url(self):
        """Returns the URL to access a detail record for this passenger."""
        return reverse('passenger-detail', args=[str(self.id)])



class Trip(models.Model):
    """Trips that passengers make"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    passenger_id = models.ForeignKey(Passenger, on_delete=models.SET_NULL, null=True)

    start_time = models.DateTimeField('Start Time', auto_now=True)

    start_point = models.CharField('Start Location', max_length=7, help_text='Enter your start location as -,-. (Ex. 12, 45)')
    end_point =  models.CharField('End Location', max_length=7, help_text='Enter your end location as -,-. (Ex. 12, 45)')

    total_distance = models.FloatField('Total Distance')

    def __str__(self):
        """String for representing the Model object."""
        return self.id

    def get_absolute_url(self):
        """Returns the URL to access a detail record for this passenger."""
        return reverse('trip-detail', args=[str(self.id)])