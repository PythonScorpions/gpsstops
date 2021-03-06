'''
'''
from django.shortcuts import render
from django.views.generic import TemplateView, UpdateView, View
from django.shortcuts import render_to_response, redirect, render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.template import RequestContext, Context
from django.contrib import messages

from accounts.forms import *
from accounts.utils import *
from maps.models import *

import datetime


def custom_login_required(f):

    def wrap(request, *args, **kwargs):
        """
           this will check user is logged in , if not it will redirect to login page
        """
        if request.user.is_authenticated(): # and request.user.is_superuser is False:
            pass
        else:
            return render_to_response('index.html', locals(), context_instance=RequestContext(request))
        return f(request, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap


class Create_Route(View):
    template1 = "add-route.html"
    template2 = "add-route.html"

    @method_decorator(custom_login_required)
    def get(self, request):
        active = "maps"
        flag="maps"
        return render(request, self.template1, locals())

    @method_decorator(custom_login_required)
    def post(self, request):
        print "came in POST"
        trip_title = request.POST['trip_title']
        trip_datetime = datetime.datetime.strptime(str(request.POST['trip_datetime']), "%b %d,%Y %I:%M %p")
        print trip_title
        print type(trip_datetime), "-----------------", trip_datetime
        total_time = request.POST['total_hours']
        total_time_opt = request.POST['opt_hours']
        print request.POST['total_distance']
        if '.' in request.POST['total_distance']:
            total_distance = float(request.POST['total_distance'][:-6])
        else:
            total_distance = float(int(request.POST['total_distance'][:-6]))

        if '.' in request.POST['opt_distance']:
            total_distance_opt = float(request.POST['opt_distance'][:-6])
        else:
            total_distance_opt = float(int(request.POST['opt_distance'][:-6]))

        start_search_address = request.POST['start_search_address']
        start_near_address = request.POST['start_near_address']
        start_note_location = request.POST['start_note_location']
        latitude_first = request.POST['latitude_first']
        longitude_first = request.POST['longitude_first']

        end_search_address = request.POST['end_search_address']
        end_near_address = request.POST['end_near_address']
        end_note_location = request.POST['end_note_location']
        latitude_last = request.POST['latitude_last']
        longitude_last = request.POST['longitude_last']

        form = RouteAssignmentForm(data=request.POST, user=request.user)
        if not form.is_valid():
            return redirect('/maps/create_route/?message=' + str(form.errors))

        route_obj = Route(
            user=form.cleaned_data['user'], trip_title=trip_title,
            trip_datetime=trip_datetime, total_distance=total_distance,
            total_time=total_time, optimized_total_distance=total_distance_opt,
            optimized_total_time=total_time_opt,
            is_editable=form.cleaned_data['is_editable'],
            created_by=request.user)
        route_obj.save()

        total_waypoint = int(request.POST['total_waypoint'])

        Location(route=route_obj, location_address=start_search_address, location_near_address=start_near_address,
                 location_lat=latitude_first, location_long=longitude_first, location_note=start_note_location,
                 location_number=11).save()
        OptimizedLocation(route=route_obj, location_address=start_search_address, location_near_address=start_near_address,
                          location_lat=latitude_first, location_long=longitude_first, location_note=start_note_location,
                          location_number=11).save()

        for i in xrange(1, total_waypoint+1):
            search_add_n = "search_address"+str(i)
            near_add_n = "near_address"+str(i)
            note_waypoint_n = "note_waypoint"+str(i)
            latitude_n = "latitude"+str(i)
            longitude_n = "longitude"+str(i)
            search_address = request.POST[search_add_n]
            near_address = request.POST[near_add_n]
            note = request.POST[note_waypoint_n]
            lat_data = request.POST[latitude_n]
            lng_data = request.POST[longitude_n]

            Location(route=route_obj, location_address=search_address, location_near_address=near_address,
                     location_lat=lat_data, location_long=lng_data, location_note=note, location_number=i).save()

        for k in xrange(1, total_waypoint+1):
            order = "order"+str(k-1)
            order_no = int(request.POST[order])+1
            # near_opt = "opt_near_address"+str(k)
            # latitude_opt = "opt_latitude"+str(i)
            # longitude_opt = "opt_longitude"+str(i)
            # near_opt_address = request.POST[near_opt]
            # latitude_opt_address = request.POST[latitude_opt]
            # longitude_opt_address = request.POST[longitude_opt]
            manual_loc_obj = Location.objects.get(location_number=order_no, route=route_obj)
            # search_add_opt = manual_loc_obj.location_address
            # note_opt = manual_loc_obj.location_note

            OptimizedLocation(route=route_obj, location_address=manual_loc_obj.location_address,
                              location_near_address=manual_loc_obj.location_near_address,
                              location_lat=manual_loc_obj.location_lat, location_long=manual_loc_obj.location_long,
                              location_note=manual_loc_obj.location_note, location_number=k).save()

        Location(route=route_obj, location_address=end_search_address, location_near_address=end_near_address,
                 location_lat=latitude_last, location_long=longitude_last, location_note=end_note_location,
                 location_number=22).save()
        OptimizedLocation(route=route_obj, location_address=end_search_address, location_near_address=end_near_address,
                          location_lat=latitude_last, location_long=longitude_last, location_note=end_note_location,
                          location_number=22).save()
        url_to_redirect = '/maps/routes/?day='+str(trip_datetime.day)+'&month='+str(trip_datetime.month)+'&year='+str(trip_datetime.year)
        return HttpResponseRedirect(url_to_redirect)


class Edit_Route(View):
    template1 = "edit-route.html"
    template2 = "add-route.html"

    @method_decorator(custom_login_required)
    def get(self, request, **kwargs):

        print "came in to get"
        id = int(self.kwargs['id'])
        route_obj = Route.objects.get(id=id)
        print route_obj.trip_title
        start_end =[11, 22]
        location_obj = Location.objects.filter(route=route_obj).order_by('id')
        for d1 in location_obj:
            print d1

        total_way_point = len(location_obj) - 2
        print total_way_point, "<--Total way point"

        active = "maps"
        flag="maps"
        today = datetime.date.today()
        routes = Route.objects.filter(user=request.user, trip_datetime__startswith=today).exclude(id=id)

        form = RouteAssignmentForm(user=request.user,
                    initial={'user':route_obj.user.id, 'is_editable':route_obj.is_editable})
        print route_obj.user, route_obj.is_editable

        return render(request, self.template1, locals())

    @method_decorator(custom_login_required)
    def post(self, request, id):
        form = RouteAssignmentForm(data=request.POST, user=request.user)
        if not form.is_valid():
            return redirect('?message=' + str(form.errors))

        print "came in POST"
        trip_title = request.POST['trip_title']
        trip_datetime = datetime.datetime.strptime(str(request.POST['trip_datetime']), "%b %d,%Y %I:%M %p")
        print trip_title
        print type(trip_datetime), "-----------------", trip_datetime
        total_time = request.POST['total_hours']
        total_time_opt = request.POST['opt_hours']
        if '.' in request.POST['total_distance']:
            total_distance = float(request.POST['total_distance'][:-6])
        else:
            total_distance = float(int(request.POST['total_distance'][:-6]))

        if '.' in request.POST['opt_distance']:
            total_distance_opt = float(request.POST['opt_distance'][:-6])
        else:
            total_distance_opt = float(int(request.POST['opt_distance'][:-6]))

        start_search_address = request.POST['start_search_address']
        start_near_address = request.POST['start_near_address']
        start_note_location = request.POST['start_note_location']
        latitude_first = request.POST['latitude_first']
        longitude_first = request.POST['longitude_first']

        end_search_address = request.POST['end_search_address']
        end_near_address = request.POST['end_near_address']
        end_note_location = request.POST['end_note_location']
        latitude_last = request.POST['latitude_last']
        longitude_last = request.POST['longitude_last']
        route_obj = Route.objects.get(id=int(id))
        route_obj.trip_title = trip_title
        route_obj.trip_datetime = trip_datetime
        route_obj.total_distance = total_distance
        route_obj.total_time = total_time
        route_obj.optimized_total_time = total_time_opt
        route_obj.optimized_total_distance = total_distance_opt
        route_obj.user = form.cleaned_data['user']
        route_obj.is_editable = form.cleaned_data['is_editable']

        route_obj.save()

        Location.objects.filter(route=route_obj).delete()
        OptimizedLocation.objects.filter(route=route_obj).delete()

        total_waypoint = int(request.POST['total_waypoint'])

        Location(route=route_obj, location_address=start_search_address, location_near_address=start_near_address,
                 location_lat=latitude_first, location_long=longitude_first, location_note=start_note_location,
                 location_number=11).save()
        OptimizedLocation(route=route_obj, location_address=start_search_address, location_near_address=start_near_address,
                          location_lat=latitude_first, location_long=longitude_first, location_note=start_note_location,
                          location_number=11).save()

        for i in xrange(1, total_waypoint+1):
            search_add_n = "search_address"+str(i)
            near_add_n = "near_address"+str(i)
            note_waypoint_n = "note_waypoint"+str(i)
            latitude_n = "latitude"+str(i)
            longitude_n = "longitude"+str(i)
            search_address = request.POST[search_add_n]
            near_address = request.POST[near_add_n]
            note = request.POST[note_waypoint_n]
            lat_data = request.POST[latitude_n]
            lng_data = request.POST[longitude_n]

            Location(route=route_obj, location_address=search_address, location_near_address=near_address,
                     location_lat=lat_data, location_long=lng_data, location_note=note, location_number=i).save()

        for k in xrange(1, total_waypoint+1):
            order = "order"+str(k-1)
            order_no = int(request.POST[order])+1
            # near_opt = "opt_near_address"+str(k)
            # latitude_opt = "opt_latitude"+str(i)
            # longitude_opt = "opt_longitude"+str(i)
            # near_opt_address = request.POST[near_opt]
            # latitude_opt_address = request.POST[latitude_opt]
            # longitude_opt_address = request.POST[longitude_opt]
            manual_loc_obj = Location.objects.get(location_number=order_no, route=route_obj)
            # search_add_opt = manual_loc_obj.location_address
            # note_opt = manual_loc_obj.location_note

            OptimizedLocation(route=route_obj, location_address=manual_loc_obj.location_address,
                              location_near_address=manual_loc_obj.location_near_address,
                              location_lat=manual_loc_obj.location_lat, location_long=manual_loc_obj.location_long,
                              location_note=manual_loc_obj.location_note, location_number=k).save()

        Location(route=route_obj, location_address=end_search_address, location_near_address=end_near_address,
                 location_lat=latitude_last, location_long=longitude_last, location_note=end_note_location,
                 location_number=22).save()
        OptimizedLocation(route=route_obj, location_address=end_search_address, location_near_address=end_near_address,
                          location_lat=latitude_last, location_long=longitude_last, location_note=end_note_location,
                          location_number=22).save()

        # trip_title = request.POST['trip_title']
        active = "maps"
        flag = "maps"
        url_to_redirect = '/maps/routes/?day='+str(trip_datetime.day)+'&month='+str(trip_datetime.month)+'&year='+str(trip_datetime.year)
        return HttpResponseRedirect(url_to_redirect)


class Routes(View):
    template1 = "routes.html"

    @method_decorator(custom_login_required)
    def get(self, request):
        if 'day' in request.GET:
            date_selected = datetime.date(
                int(request.GET['year']),
                int(request.GET['month']),
                int(request.GET['day']))
            messages.success(request, "Your Route has been saved")
        else:
            date_selected = datetime.date.today()

        routes = filter_objects_by_user(request.user, Route)
        routes = routes.filter(trip_datetime__startswith=date_selected)
        print routes

        active = "maps"
        flag = "maps"
        return render_to_response(self.template1, locals(), context_instance=RequestContext(request))
        # return render(request, self.template1, locals())

    @method_decorator(custom_login_required)
    @method_decorator(csrf_exempt)
    def post(self, request):
        day_selected = int(request.POST['day'])
        month_selected = int(request.POST['month'])
        year_selected = int(request.POST['year'])
        date_selected = datetime.date(year_selected, month_selected, day_selected)
        print date_selected
        routes = Route.objects.filter(user=request.user, trip_datetime__startswith=date_selected)
        return render(request, self.template1, locals())


class Optimized_Route(View):
    template1 = "optimum-route.html"

    @method_decorator(custom_login_required)
    def get(self, request, **kwargs):
        id = int(self.kwargs['id'])
        route_obj = Route.objects.get(id=id)
        print route_obj.trip_title
        start_end =[11, 22]
        location_obj = OptimizedLocation.objects.filter(route=route_obj).order_by('id')
        for d1 in location_obj:
            print d1

        total_way_point = len(location_obj) - 2
        print total_way_point, "<--Total way point"

        active = "maps"
        flag="maps"
        today = datetime.date.today()

        routes = Route.objects.filter(user=request.user, trip_datetime__startswith=today).exclude(id=id)

        return render(request, self.template1, locals())