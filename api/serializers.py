from rest_framework import serializers
from django.contrib.auth.models import User
from accounts.models import UserProfiles
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from maps.models import *
from rest_framework import exceptions, serializers


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