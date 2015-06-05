from django.shortcuts import render
from django.views.generic import TemplateView, UpdateView, View
from django.shortcuts import render_to_response, redirect, render
from maps.models import *
import datetime
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class Create_Route(View):
    template1 = "add-route.html"
    template2 = "add-route.html"

    @method_decorator(login_required)
    def get(self, request):
        active = "maps"
        flag="maps"
        return render(request, self.template1, locals())

    @method_decorator(login_required)
    def post(self, request):
        print "came in POST"
        trip_title = request.POST['trip_title']
        trip_datetime = datetime.datetime.strptime(str(request.POST['trip_datetime']), "%Y/%m/%d %H:%M")
        print trip_title
        print type(trip_datetime), "-----------------", trip_datetime
        total_time = request.POST['total_hours']
        if '.' in request.POST['total_distance']:
            total_distance = float(request.POST['total_distance'][:-3])
        else:
            total_distance = float(int(request.POST['total_distance'][:-3]))

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
        route_obj = Route(user=request.user, trip_title=trip_title, trip_datetime=trip_datetime,
                          total_distance=total_distance, total_time=total_time)
        route_obj.save()

        total_waypoint = int(request.POST['total_waypoint'])

        Location(route=route_obj, location_address=start_search_address, location_near_address=start_near_address,
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

        Location(route=route_obj, location_address=end_search_address, location_near_address=end_near_address,
                 location_lat=latitude_last, location_long=longitude_last, location_note=end_note_location,
                 location_number=22).save()

        # trip_title = request.POST['trip_title']
        active = "maps"
        flag = "maps"
        return HttpResponseRedirect('/maps/routes')


class Edit_Route(View):
    template1 = "edit-route.html"
    template2 = "add-route.html"

    @method_decorator(login_required)
    def get(self, request, **kwargs):
        print "came in to get"
        id = int(self.kwargs['id'])
        route_obj = Route.objects.get(id=id)
        print route_obj.trip_title
        start_end =[11, 22]
        location_obj = Location.objects.filter(route = route_obj).order_by('id')
        for d1 in location_obj:
            print d1

        total_way_point = len(location_obj) - 2
        print total_way_point, "<--Total way point"

        active = "maps"
        flag="maps"
        today = datetime.date.today()
        routes = Route.objects.filter(user=request.user, trip_datetime__startswith=today).exclude(id=id)

        return render(request, self.template1, locals())

    @method_decorator(login_required)
    def post(self, request, id):
        print "came in POST"
        trip_title = request.POST['trip_title']
        trip_datetime = datetime.datetime.strptime(str(request.POST['trip_datetime']), "%Y/%m/%d %H:%M")
        print trip_title
        print type(trip_datetime), "-----------------", trip_datetime
        total_time = request.POST['total_hours']
        if '.' in request.POST['total_distance']:
            total_distance = float(request.POST['total_distance'][:-3])
        else:
            total_distance = float(int(request.POST['total_distance'][:-3]))

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

        route_obj.save()

        Location.objects.filter(route=route_obj).delete()

        total_waypoint = int(request.POST['total_waypoint'])

        Location(route=route_obj, location_address=start_search_address, location_near_address=start_near_address,
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

        Location(route=route_obj, location_address=end_search_address, location_near_address=end_near_address,
                 location_lat=latitude_last, location_long=longitude_last, location_note=end_note_location,
                 location_number=22).save()

        # trip_title = request.POST['trip_title']
        active = "maps"
        flag = "maps"
        return HttpResponseRedirect('/maps/routes')


class Routes(View):
    template1 = "routes.html"

    @method_decorator(login_required)
    def get(self, request):
        today = datetime.date.today()
        routes = Route.objects.filter(user=request.user, trip_datetime__startswith=today)
        print routes
        active = "maps"
        flag = "maps"
        return render(request, self.template1, locals())