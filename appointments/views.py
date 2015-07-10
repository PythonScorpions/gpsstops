'''
'''
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse

from appointments.forms import *

import json


class AppointmentView(View):
    def get(self, request, *args, **kwargs):
        form = AppointmentForm()
        return render(request, "appointment.html", {'form':form})

    def post(self, request, *args, **kwargs):
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save();
            return HttpResponse(json.dumps({'status':'success'}), content_type="application/json")
        else:
            return render(request, "appointment.html", {'form':form})
appointment_view = AppointmentView.as_view()
