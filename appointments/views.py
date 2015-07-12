'''
'''
from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpResponse

from appointments.forms import *

import json


class AppointmentView(View):
    def get(self, request, *args, **kwargs):
        form = AppointmentForm()
        return render(request, "calendar/appointments.html", {'form':form})

    def post(self, request, *args, **kwargs):
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            # return HttpResponse(json.dumps({'status':'success'}), content_type="application/json")
            return redirect("/calendar/")
        else:
            print form.errors
            return render(request, "calendar/appointments.html", {'form':form})
appointment_view = AppointmentView.as_view()


class TaskView(View):
    def get(self, request, *args, **kwargs):
        form = TaskForm()
        return render(request, "calendar/task.html", {'form':form})

    def post(self, request, *args, **kwargs):
        form = TaskForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save();
            return HttpResponse(json.dumps({'status':'success'}), content_type="application/json")
        else:
            return render(request, "calendar/task.html", {'form':form})
task_view = TaskView.as_view()
