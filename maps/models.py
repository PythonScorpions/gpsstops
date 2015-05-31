from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Route(models.Model):
    user = models.ForeignKey(User)
    trip_title = models.CharField(max_length=100, blank=True, null=True)
    total_distance = models.FloatField(default=0.0)
    total_time = models.CharField(max_length=30, blank=True, null=True)
    trip_datetime = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)


class Location(models.Model):
    route = models.ForeignKey(Route, related_name='route_locations')
    location_address = models.CharField(max_length=200, blank=True, null=True)
    location_near_address = models.CharField(max_length=200, blank=True, null=True)
    location_lat = models.DecimalField(max_digits=19, decimal_places=15,blank=True, null=True)
    location_long = models.DecimalField(max_digits=19, decimal_places=15,blank=True, null=True)
    location_note = models.CharField(max_length=200, blank=True, null=True)
    location_number = models.IntegerField(default=0)
