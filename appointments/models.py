'''
'''
from django.db import models
from django.contrib.auth.models import User


class Appointments(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=100)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    timezone = models.CharField(max_length=100, default='Asia/Kolkatta') # Exhaustive list https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
    where = models.CharField(max_length=500)
    all_day = models.BooleanField(default=False)
    repeat = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return "%s - %s (%s - %s)" % (self.user, self.title,
            self.start_datetime, self.end_datetime)



class Notifications(models.Model):
    NOTIFICATIONS_TYPES = (
        ('email', 'Email'),
        ('pop_up', 'Pop-up'),
    )

    UNIT_TYPES = (
        ('minutes', 'minutes'),
        ('hours', 'hours'),
        ('days', 'days'),
        ('weeks', 'weeks'),
    )

    appointments = models.ForeignKey(Appointments)
    notification_type = models.CharField(max_length=10, choices=NOTIFICATIONS_TYPES)
    value = models.IntegerField()
    units = models.CharField(max_length=10, choices=UNIT_TYPES)



class Task(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=100)
    due_date = models.DateField()

    def __unicode__(self):
        return "%s - %s" % (self.user, self.title)


class TaskNotifications(models.Model):
    NOTIFICATIONS_TYPES = (
        ('email', 'Email'),
        ('pop_up', 'Pop-up'),
    )

    UNIT_TYPES = (
        ('minutes', 'minutes'),
        ('hours', 'hours'),
        ('days', 'days'),
        ('weeks', 'weeks'),
    )

    task = models.ForeignKey(Task)
    notification_type = models.CharField(max_length=10, choices=NOTIFICATIONS_TYPES)
    value = models.IntegerField()
    units = models.CharField(max_length=10, choices=UNIT_TYPES)



class ContactGroup(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=300)
    remarks = models.TextField(blank=True, null=True)


class Contact(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=300)
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=300, blank=True, null=True)
    address_line_1 = models.CharField(max_length=300)
    address_line_2 = models.CharField(max_length=300, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=300)
    zipcode = models.CharField(max_length=20)
    mobile = models.CharField(max_length=15)
    office = models.CharField(max_length=20, blank=True, null=True)
    email_1 = models.EmailField(blank=True, null=True)
    email_2 = models.EmailField(blank=True, null=True)
    contact_group = models.ForeignKey(ContactGroup, blank=True, null=True)

