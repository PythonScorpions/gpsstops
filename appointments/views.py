'''
'''
from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpResponse, HttpResponseServerError

from appointments.forms import *

import json, datetime


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
            form.instance.location = form.cleaned_data['where']
            form.save()
            # return HttpResponse(json.dumps({'status':'success'}), content_type="application/json")
            return redirect("/calender/")
        else:
            print form.errors
            return render(request, "calendar/appointments.html", {'form':form})
appointment_view = AppointmentView.as_view()


class DateForm(forms.Form):
    date = forms.DateField()


class EventView(View):
    def get(self, request, pk=None, *args, **kwargs):
        try:
            appointment = Appointments.objects.get(pk=pk)
        except:
            pass
        else:
            form = DateForm(request.GET)
            if form.is_valid():
                curdt = appointment.start_datetime
                newdt = datetime.datetime(
                        form.cleaned_data['date'].year,
                        form.cleaned_data['date'].month,
                        form.cleaned_data['date'].day,
                        curdt.hour,
                        curdt.minute,
                        curdt.second
                    )

                appointment.start_datetime = newdt
                appointment.save()
                return HttpResponse('success')
        return HttpResponseServerError('object not found')
event_view = EventView.as_view()

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


class TaskEventView(View):
    def get(self, request, pk=None, *args, **kwargs):
        try:
            task = Task.objects.get(pk=pk)
        except:
            pass
        else:
            form = DateForm(request.GET)
            if form.is_valid():
                task.due_date = form.cleaned_data['date']
                task.save()
                return HttpResponse('success')
        return HttpResponseServerError('object not found')
task_event_view = TaskEventView.as_view()