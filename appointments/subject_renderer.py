'''
'''
from appointments.models import *


def get_appointments():
    print "reached"
    return {
        'name': notification.subject.name,
        'timestamp': str(now()),
        'icon': kwargs.get('icon')
    }
