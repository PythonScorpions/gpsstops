'''
Appointments app
'''
from django.conf.urls import patterns, include, url

from appointments.views import *

urlpatterns = patterns('',
    url(r'^create/$', appointment_view, name='create_appointment'),
    url(r'^(?P<pk>\d+)/$', appointment_view, name='edit_appointment'),
    url(r'^event/(?P<pk>\d+)/move/$', event_view, name='move_appointment'),

    url(r'^task/create/$', task_view, name='create_task'),
    url(r'^task/(?P<pk>\d+)/$', task_view, name='edit_task'),
    url(r'^event/task/(?P<pk>\d+)/move/$', task_event_view, name='move_task'),

    url(r'^agenda/$', agenda_view, name='get_agendas'),

    url(r'^contact_group/$', contactgroup_list_view, name='list_contact_group'),
    url(r'^contact_group/create/$', contactgroup_view, name='create_contact_group'),
    url(r'^contact_group/(?P<pk>\d+)/$', contactgroup_view, name='edit_contact_group'),

    url(r'^contact/$', contact_list_view, name='list_contact'),
    url(r'^contact/create/$', contact_view, name='create_contact'),
    url(r'^contact/(?P<pk>\d+)/$', contact_view, name='edit_contact')
)
