'''
'''
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework import exceptions, serializers

from accounts.models import UserProfiles
from appointments.models import *
from maps.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfiles
        exclude = ('id', 'user', 'token')


class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            print "fkk"
            user = authenticate(username=username, password=password)

            if not user:
                print "jfdjk"
                msg = _('Unable to log in with provided credentials.')
                raise exceptions.ValidationError(msg)
        else:
            msg = _('Must include "username" and "password"')
            raise exceptions.ValidationError(msg)

        attrs['user'] = user
        return attrs


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location


class OptLocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = OptimizedLocation


class RouteSerializer(serializers.ModelSerializer):
    locations = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    trip_datetime = serializers.SerializerMethodField()

    class Meta:
        model = Route

    @staticmethod
    def get_locations(obj):

        all_locations = Location.objects.filter(route=obj)
        location_data = LocationSerializer(all_locations, many=True)
        return location_data.data

    @staticmethod
    def get_created_at(obj):

        created = str(obj.created_at).split(' ')
        return created[0].replace('-', '/') + ' ' + created[1][:5]

    @staticmethod
    def get_updated_at(obj):

        updated = str(obj.updated_at).split(' ')
        return updated[0].replace('-', '/') + ' ' + updated[1][:5]

    @staticmethod
    def get_trip_datetime(obj):

        triptime = str(obj.trip_datetime).split(' ')
        return triptime[0].replace('-', '/') + ' ' + triptime[1][:5]


class OptRouteSerializer(serializers.ModelSerializer):
    locations = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    trip_datetime = serializers.SerializerMethodField()

    class Meta:
        model = Route

    @staticmethod
    def get_locations(obj):

        all_locations = OptimizedLocation.objects.filter(route=obj)
        location_data = OptLocationSerializer(all_locations, many=True)
        return location_data.data

    @staticmethod
    def get_created_at(obj):

        created = str(obj.created_at).split(' ')
        return created[0].replace('-', '/') + ' ' + created[1][:5]

    @staticmethod
    def get_updated_at(obj):

        updated = str(obj.updated_at).split(' ')
        return updated[0].replace('-', '/') + ' ' + updated[1][:5]

    @staticmethod
    def get_trip_datetime(obj):

        triptime = str(obj.trip_datetime).split(' ')
        return triptime[0].replace('-', '/') + ' ' + triptime[1][:5]



class AppointmentsSerializer(serializers.ModelSerializer):
    start_datetime = serializers.DateTimeField(
                        format="%m/%d/%Y %I:%M %p",
                        input_formats=["%m/%d/%Y %I:%M %p"])

    class Meta:
        model = Appointments
        fields = ('id', 'user', 'title', 'start_datetime', 'timezone',
                    'location', 'latitude', 'longitude',
                    'repeat_days', 'description', 'notification_required',
                    'notification_time')

    def create(self, validated_data):
         appointments = Appointments.objects.create(
            user=validated_data['user'],
            title=validated_data['title'],
            start_datetime=validated_data['start_datetime'],
            timezone=validated_data['timezone'],
            location=validated_data['location'],
            latitude=validated_data['latitude'],
            longitude=validated_data['longitude'],
            where=validated_data['location'],
            repeat_days=validated_data['repeat_days'],
            description=validated_data['description'],
            notification_time=validated_data['notification_time'],
            notification_required=validated_data['notification_required']
         )
         return appointments



class TaskSerializer(serializers.ModelSerializer):
    due_date = serializers.DateTimeField(
                        format="%m/%d/%Y %I:%M %p",
                        input_formats=["%m/%d/%Y %I:%M %p"])

    class Meta:
        model = Task
        fields = ('id', 'user', 'title', 'due_date', 'timezone', 'note',
                    'notification_required', 'notification_time')

    def create(self, validated_data):
        task = Task.objects.create(
            user=validated_data['user'],
            title=validated_data['title'],
            due_date=validated_data['due_date'],
            timezone=validated_data['timezone'],
            note=validated_data['note'],
            notification_time=validated_data['notification_time'],
            notification_required=validated_data['notification_required']
        )
        return task


class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contacts
        fields = ('id', 'user', 'name', 'title', 'company', 'location',
                    'latitude', 'longitude', 'city', 'state', 'zipcode', 'cell_phone',
                    'office_phone', 'email1', 'email2', 'group')

    def create(self, validated_data):
        contact = Contacts.objects.create(
            user=validated_data['user'],
            name=validated_data['name'],
            title=validated_data['title'],
            company=validated_data['company'],
            location=validated_data['location'],
            latitude=validated_data['latitude'],
            longitude=validated_data['longitude'],
            city=validated_data['city'],
            state=validated_data['state'],
            zipcode=validated_data['zipcode'],
            cell_phone=validated_data['cell_phone'],
            office_phone=validated_data['office_phone'],
            email1=validated_data['email1'],
            email2=validated_data['email2'],
            group=validated_data['group']
        )
        return contact


class ContactGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContactGroup
        fields = ('id', 'user', 'name', 'remarks')

    def create(self, validated_data):
        contact_group = ContactGroup.objects.create(
            user=validated_data['user'],
            name=validated_data['name'],
            remarks=validated_data['remarks']
        )
        return contact_group

