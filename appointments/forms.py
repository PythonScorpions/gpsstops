'''
'''
from django import forms
from django.contrib.auth.models import User
from django.db.models import Q

from appointments.models import *

def _get_users(user):
    if user.user_profiles.user_role == "super_admin":
        users = User.objects \
                .filter(
                    Q(user_profiles__admin=user) |
                    Q(user_profiles__admin__user_profiles__admin=user)
                ) \
                .exclude(pk=user.id)
    else:
        users = User.objects \
                .filter(
                    Q(user_profiles__admin=user) |
                    Q(user_profiles__admin=user.user_profiles.admin)
                ) \
                .filter(user_profiles__user_role="employee") \
                .exclude(pk=user.id)

    return users

class AppointmentForm(forms.ModelForm):
    start_datetime = forms.DateTimeField(input_formats=["%b %d,%Y %I:%M %p"])
    latitude = forms.FloatField(widget=forms.widgets.HiddenInput())
    longitude = forms.FloatField(widget=forms.widgets.HiddenInput())

    def __init__(self, user, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        self.user = user

        users_choices = [(self.user.id, 'Self')]
        for u in _get_users(self.user):
            users_choices.append((u.id, '%s %s' % (u.first_name, u.last_name)))
        self.fields['user'].choices = users_choices

    class Meta:
        model = Appointments
        exclude = ('location', 'created_by')


class TaskForm(forms.ModelForm):
    due_date = forms.DateTimeField(
        input_formats=["%b %d,%Y %I:%M %p"])

    def __init__(self, user, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.user = user

        users_choices = [(self.user.id, 'Self')]
        for u in _get_users(self.user):
            users_choices.append((u.id, '%s %s' % (u.first_name, u.last_name)))
        self.fields['user'].choices = users_choices

    class Meta:
        model = Task
        exclude = ('created_by',)


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contacts
        exclude = ('user','latitude','longitude')

class ContactGroupForm(forms.ModelForm):
    class Meta:
        model = ContactGroup
        exclude = ('user',)