'''
'''
from django import forms
from django.contrib.auth.models import User

from appointments.models import *


class AppointmentForm(forms.ModelForm):
    start_datetime = forms.DateTimeField(
        input_formats=["%b %d,%Y %I:%M %p"])

    class Meta:
        model = Appointments
        exclude = ('user',)


class TaskForm(forms.ModelForm):
    due_date = forms.DateTimeField(
        input_formats=["%b %d,%Y %I:%M %p"])

    class Meta:
        model = Task
        exclude = ('user',)
