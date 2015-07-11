'''
'''
from django import forms
from django.contrib.auth.models import User

from appointments.models import *


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointments
        exclude = ('user',)


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ('user',)
