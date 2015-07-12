'''
'''
from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpResponse

from appointments.forms import *

import json


class AppointmentView(View):
    def get(self, request, pk=None, *args, **kwargs):
        appointment = None
        try:
            appointment = Appointments.objects.get(id=pk)
        except:
            redirect('/appointments/create/')

        if appointment:
            form = AppointmentForm(instance=appointment)
        else:
            form = AppointmentForm()

        return render(request, "calendar/appointments.html", {'form':form})

    def post(self, request, pk=None, *args, **kwargs):
        appointment = None
        try:
            appointment = Appointments.objects.get(id=pk)
        except:
            redirect('/appointments/create/')

        if appointment:
            form = AppointmentForm(request.POST, instance=appointment)
        else:
            form = AppointmentForm(request.POST)

        if form.is_valid():
            form.instance.user = request.user
            form.save()
            # return HttpResponse(json.dumps({'status':'success'}), content_type="application/json")
            return redirect("/calender/")
        else:
            print form.errors
            return render(request, "calendar/appointments.html", {'form':form})
appointment_view = AppointmentView.as_view()


class TaskView(View):
    def get(self, request, pk=None, *args, **kwargs):
        task = None
        try:
            task = Task.objects.get(id=pk)
        except:
            redirect('/task/create/')

        if task:
            form = TaskForm(instance=task)
        else:
            form = TaskForm()

        return render(request, "calendar/task.html", {'form':form})

    def post(self, request, pk=None, *args, **kwargs):
        task = None
        try:
            task = Task.objects.get(id=pk)
        except:
            redirect('/task/create/')

        if task:
            form = TaskForm(request.POST, instance=task)
        else:
            form = TaskForm(request.POST)

        if form.is_valid():
            form.instance.user = request.user
            form.save();
            return redirect('/calender/')
        else:
            return render(request, "calendar/task.html", {'form':form})
task_view = TaskView.as_view()
