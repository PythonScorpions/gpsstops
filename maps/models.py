from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Route(models.Model):
    user = models.ForeignKey(User)
    trip_title = models.CharField(max_length=100, blank=True, null=True)
    total_distance = models.FloatField(default=0.0)
    optimized_total_distance = models.FloatField(default=0.0)
    optimized_total_time = models.CharField(max_length=30, blank=True, null=True)
    total_time = models.CharField(max_length=30, blank=True, null=True)
    trip_datetime = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    is_editable = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, related_name='route_created_by', null=True)

    def __unicode(self):
        return u'%s' % self.trip_title


class Location(models.Model):
    route = models.ForeignKey(Route, related_name='route_locations')
    location_address = models.CharField(max_length=200, blank=True, null=True)
    location_near_address = models.CharField(max_length=200, blank=True, null=True)
    location_lat = models.FloatField(default=0.0)
    location_long = models.FloatField(default=0.0)
    location_note = models.CharField(max_length=200, blank=True, null=True)
    location_number = models.IntegerField(default=0)
    distance = models.CharField(max_length=200, blank=True, null=True)
    time = models.CharField(max_length=200, blank=True, null=True)

    def __unicode(self):
        return u'%s' % self.route


class OptimizedLocation(models.Model):
    route = models.ForeignKey(Route, related_name='optimized_route_locations')
    location_address = models.CharField(max_length=200, blank=True, null=True)
    location_near_address = models.CharField(max_length=200, blank=True, null=True)
    location_lat = models.FloatField(default=0.0)
    location_long = models.FloatField(default=0.0)
    location_note = models.CharField(max_length=200, blank=True, null=True)
    location_number = models.IntegerField(default=0)
    distance = models.CharField(max_length=200, blank=True, null=True)
    time = models.CharField(max_length=200, blank=True, null=True)

    def __unicode(self):
        return u'%s' % self.route