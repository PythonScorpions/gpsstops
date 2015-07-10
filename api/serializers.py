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
    user_id = serializers.IntegerField()

    class Meta:
        model = Appointments
        fields = ('id', 'title', 'start_datetime', 'end_datetime', 'timezone',
                    'location', 'latitude', 'longitude', 'where', 'all_day',
                    'repeat', 'description', 'notification_required',
                    'notification_time')

    def validate_user_id(self, value):
        try:
            user = User.objects.get(id=value)
        except:
            raise serializers.ValidationError("User not found")
        else:
            if not user.is_active:
                raise serializers.ValidationError("User not found")
        return user

    def create(self, validated_data):
        appointments = Appointments.objects.create(
            user=validated_data['user'],
            title=validated_data['title'],
            start_datetime=validated_data['start_datetime'],
            end_datetime=validated_data['end_datetime'],
            timezone=validated_data['timezone'],
            location=validated_data['location'],
            latitude=validated_data['latitude'],
            longitude=validated_data['longitude'],
            where=validated_data['where'],
            all_day=validated_data['all_day'],
            repeat=validated_data['repeat'],
            description=validated_data['description'],
            notification_time=validated_data['notification_time'],
            notification_required=validated_data['notification_required']
        )
        return appointments


class TaskSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()

    class Meta:
        model = Task
        fields = ('id', 'title', 'due_date', 'timezone', 'note',
                    'notification_required', 'notification_time')

    def validate_user_id(self, value):
        try:
            user = User.objects.get(id=value)
        except:
            raise serializers.ValidationError("User not found")
        else:
            if not user.is_active:
                raise serializers.ValidationError("User not found")
        return user

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
    user_id = serializers.IntegerField()
    group_id = serializers.IntegerField()

    class Meta:
        model = Contact
        fields = ('id', 'name', 'title', 'company', 'address_line_1',
                    'address_line_2', 'city', 'state', 'zipcode', 'mobile',
                    'office', 'email_1', 'email_2')

    def validate_user_id(self, value):
        try:
            user = User.objects.get(id=value)
        except:
            raise serializers.ValidationError("User not found")
        else:
            if not user.is_active:
                raise serializers.ValidationError("User not found")
        return user

    def validate_group_id(self, value):
        try:
            group = ContactGroup.objects.get(id=value)
        except:
            raise serializers.ValidationError("Group not found")
        return group

    def create(self, validated_data):
        contact = Contact.objects.create(
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
            group=validated_data['group_id']
        )
        return contact


class ContactGroupSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()

    class Meta:
        model = ContactGroup
        fields = ('id', 'name', 'remarks')

    def validate_user_id(self, value):
        try:
            user = User.objects.get(id=value)
        except:
            raise serializers.ValidationError("User not found")
        else:
            if not user.is_active:
                raise serializers.ValidationError("User not found")
        return user

    def create(self, validated_data):
        contact_group = ContactGroup.objects.create(
            user=validated_data['user'],
            name=validated_data['name'],
            remarks=validated_data['remarks']
        )
        return contact_group

