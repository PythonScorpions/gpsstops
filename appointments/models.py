'''
'''
from django.db import models
from django.contrib.auth.models import User

from appointments.constants import *


class Appointments(models.Model):

    user = models.ForeignKey(User)
    title = models.CharField(max_length=100)
    start_datetime = models.DateTimeField()
    # end_datetime = models.DateTimeField(null=True, blank=True)
    timezone = models.CharField(max_length=100, default='Asia/Calcutta',
                choices=TIMEZONE_CHOICES) # Exhaustive list https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
    location = models.CharField(max_length=300)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    where = models.CharField(max_length=500)
    all_day = models.BooleanField(default=False)
    repeat = models.BooleanField(default=False)
    repeat_days = models.CommaSeparatedIntegerField(max_length=100)
    description = models.TextField(blank=True, null=True)
    notification_required = models.BooleanField(default=False)
    notification_time = models.IntegerField(choices=NOTIFICATIONS_TIME_CHOICES, default=0)

    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s - %s (%s)" % (self.user, self.title, self.start_datetime)


class Task(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=100)
    due_date = models.DateField()
    timezone = models.CharField(max_length=100, default='Asia/Kolkatta')
    note = models.TextField(blank=True, null=True)
    notification_required = models.BooleanField(default=False)
    notification_time = models.IntegerField(choices=NOTIFICATIONS_TIME_CHOICES, default=0)

    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s - %s" % (self.user, self.title)


class ContactGroup(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=300)
    remarks = models.TextField(blank=True, null=True)

    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name


class Contacts(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=300)
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=300, blank=True, null=True)
    location = models.CharField(max_length=300)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=300)
    zipcode = models.CharField(max_length=20)
    cell_phone = models.CharField(max_length=15)
    office_phone = models.CharField(max_length=20, blank=True, null=True)
    email1 = models.EmailField(blank=True, null=True)
    email2 = models.EmailField(blank=True, null=True)
    group = models.ForeignKey(ContactGroup, blank=True, null=True)

    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
