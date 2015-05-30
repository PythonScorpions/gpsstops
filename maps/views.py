from django.shortcuts import render
from django.views.generic import TemplateView, UpdateView, View
from django.shortcuts import render_to_response, redirect, render
from maps.models import *
import datetime

# Create your views here.

class Create_Route(View):
    template1 = "add-route.html"
    template2 = "add-route.html"

    def get(self, request):
        active = "maps"
        flag="maps"
        return render(request, self.template1, locals())

    def post(self, request):
        print "came in POST"
        trip_title = request.POST['trip_title']
        trip_datetime = datetime.datetime.strptime(str(request.POST['trip_datetime']), "%m/%d/%Y %I:%M %p")
        print trip_title
        print type(trip_datetime),"-----------------",trip_datetime
        raw_input("wait here")
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
        route_obj = Route(user=request.user, trip_title=trip_title, trip_datetime=trip_datetime, total_distance=total_distance,
        total_time=total_time)
        route_obj.save()

        total_waypoint = int(request.POST['total_waypoint'])

        Location(route=route_obj,location_address = start_search_address, location_near_address= start_near_address,
        location_lat=latitude_first, location_long=longitude_first,location_note=start_note_location, location_number=11).save()

        Location(route=route_obj,location_address = end_search_address, location_near_address= end_near_address,
        location_lat=latitude_last, location_long=longitude_last,location_note=end_note_location, location_number=22).save()


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

            Location(route=route_obj,location_address = search_address, location_near_address= near_address,
            location_lat=lat_data, location_long=lng_data, location_note=note, location_number=i).save()

        # trip_title = request.POST['trip_title']
        active = "maps"
        flag="maps"
        return render(request, self.template2, locals())
