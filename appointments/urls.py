'''
Appointments app
'''
from django.conf.urls import patterns, include, url

from appointments.views import *

urlpatterns = patterns('',
    url(r'create/$', appointment_view),
    url(r'task/create/$', task_view),
)
