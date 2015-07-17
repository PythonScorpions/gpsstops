'''
Appointments app
'''
from django.conf.urls import patterns, include, url

from appointments.views import *

urlpatterns = patterns('',
    url(r'^create/$', appointment_view),
    url(r'^(?P<pk>\d+)/$', appointment_view),
    url(r'^event/(?P<pk>\d+)/move/$', event_view),
    url(r'^event/task/(?P<pk>\d+)/move/$', task_event_view),

    url(r'^task/create/$', task_view),
    url(r'^task/(?P<pk>\d+)/$', task_view),

    url(r'^contact_group/$', contactgroup_list_view),
    url(r'^contact_group/create/$', contactgroup_view),
    url(r'^contact_group/(?P<pk>\d+)/$', contactgroup_view),

    url(r'^contact/$', contact_list_view),
    url(r'^contact/create/$', contact_view),
    url(r'^contact/(?P<pk>\d+)/$', contact_view)
)
