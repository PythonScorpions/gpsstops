'''
'''
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q

from rest_framework import serializers
from rest_framework import exceptions, serializers

from accounts.models import UserProfiles
from appointments.models import *
from maps.models import *

from os import urandom
import datetime, random, string


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
            # print "fkk"
            user = authenticate(username=username, password=password)

            if not user:
                # print "jfdjk"
                msg = _('Unable to log in with provided credentials.')
                raise exceptions.ValidationError(msg)
        else:
            msg = _('Must include "username" and "password"')
            raise exceptions.ValidationError(msg)

        attrs['user'] = user
        return attrs


class DeviceTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    device_token = serializers.CharField()
    device_type = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            # print "fkk"
            user = authenticate(username=username, password=password)

            if not user:
                # print "jfdjk"
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

    def to_representation(self, obj):
        result = super(RouteSerializer, self).to_representation(obj)
        result['assigned_first_name'] = obj.user.first_name
        result['assigned_last_name'] = obj.user.last_name
        result['created_by_first_name'] = obj.created_by.first_name
        result['created_by_last_name'] = obj.created_by.last_name
        return result

    @staticmethod
    def get_locations(obj):
        all_locations = Location.objects.filter(route=obj)
        location_data = LocationSerializer(all_locations, many=True)
        return location_data.data

    @staticmethod
    def get_created_at(obj):
        return obj.created_at.strftime("%m/%d/%Y %I:%M %p")
        # created = str(obj.created_at).split(' ')
        # return created[0].replace('-', '/') + ' ' + created[1][:5]

    @staticmethod
    def get_updated_at(obj):
        return obj.updated_at.strftime("%m/%d/%Y %I:%M %p")
        # updated = str(obj.updated_at).split(' ')
        # return updated[0].replace('-', '/') + ' ' + updated[1][:5]

    @staticmethod
    def get_trip_datetime(obj):
        return obj.trip_datetime.strftime("%m/%d/%Y %I:%M %p")
        # triptime = str(obj.trip_datetime).split(' ')
        # return triptime[0].replace('-', '/') + ' ' + triptime[1][:5]


class OptRouteSerializer(serializers.ModelSerializer):
    locations = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    trip_datetime = serializers.SerializerMethodField()

    class Meta:
        model = Route

    def to_representation(self, obj):
        result = super(RouteSerializer, self).to_representation(obj)
        result['assigned_first_name'] = obj.user.first_name
        result['assigned_last_name'] = obj.user.last_name
        result['created_by_first_name'] = obj.created_by.first_name
        result['created_by_last_name'] = obj.created_by.last_name
        return result

    @staticmethod
    def get_locations(obj):

        all_locations = OptimizedLocation.objects.filter(route=obj)
        location_data = OptLocationSerializer(all_locations, many=True)
        return location_data.data

    @staticmethod
    def get_created_at(obj):
        return obj.created_at.strftime("%m/%d/%Y %I:%M %p")
        # created = str(obj.created_at).split(' ')
        # return created[0].replace('-', '/') + ' ' + created[1][:5]

    @staticmethod
    def get_updated_at(obj):
        return obj.updated_at.strftime("%m/%d/%Y %I:%M %p")
        # updated = str(obj.updated_at).split(' ')
        # return updated[0].replace('-', '/') + ' ' + updated[1][:5]

    @staticmethod
    def get_trip_datetime(obj):
        return obj.trip_datetime.strftime("%m/%d/%Y %I:%M %p")
        # triptime = str(obj.trip_datetime).split(' ')
        # return triptime[0].replace('-', '/') + ' ' + triptime[1][:5]


class AppointmentsSerializer(serializers.ModelSerializer):
    start_datetime = serializers.DateTimeField(
                        format="%m/%d/%Y %I:%M %p",
                        input_formats=["%m/%d/%Y %I:%M %p"])
    assigned_user_id = serializers.IntegerField()

    class Meta:
        model = Appointments
        fields = ('id', 'user', 'title', 'start_datetime', 'timezone',
                    'location', 'latitude', 'longitude',
                    'repeat_days', 'description', 'notification_required',
                    'notification_time', 'is_editable', 'assigned_user_id')

    def to_representation(self, obj):
        result = {
            'id':obj.id,
            'user':obj.created_by.id,
            'title':obj.title,
            'start_datetime':obj.start_datetime.strftime("%m/%d/%Y %I:%M %p"),
            'timezone':obj.timezone,
            'location':obj.location,
            'latitude':obj.latitude,
            'longitude':obj.longitude,
            'repeat_days':obj.repeat_days,
            'description':obj.description,
            'notification_required':obj.notification_required,
            'notification_time':obj.notification_time,
            'is_editable':obj.is_editable,
            'created_by':obj.created_by.id,
            'created_by_first_name':obj.created_by.first_name,
            'created_by_last_name':obj.created_by.last_name
        }
        try:
            if self.assigned_user:
                result['assigned_user_id'] = self.assigned_user.id
                result['assigned_user_first_naem'] = self.assigned_user.first_name
                result['assigned_user_last_name'] = self.assigned_user.last_name
        except:
            result['assigned_user_id'] = obj.user.id
            result['assigned_user_first_name'] = obj.user.first_name
            result['assigned_user_last_name'] = obj.user.last_name
        return result


    def validate(self, data):
        try:
            user = User.objects \
                    .filter(
                        Q(user_profiles__admin=data['user']) |
                        Q(user_profiles__admin__user_profiles__admin=data['user'])
                    ) \
                    .get(pk=data['assigned_user_id'])
        except:
            raise serializers.ValidationError("Assigned user doesn't exists.")
        else:
            self.assigned_user = user
        return data

    def create(self, validated_data):
        appointments = Appointments.objects.create(
            user=self.assigned_user,
            created_by=validated_data['user'],
            is_editable=validated_data['is_editable'],
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

    def update(self, instance, validated_data):
        appointment = super(AppointmentsSerializer, self).update(instance, validated_data)
        # print appointment
        appointment.user = self.assigned_user
        appointment.save()
        return appointment



class TaskSerializer(serializers.ModelSerializer):
    due_date = serializers.DateTimeField(
                        format="%m/%d/%Y %I:%M %p",
                        input_formats=["%m/%d/%Y %I:%M %p"])
    assigned_user_id = serializers.IntegerField()

    class Meta:
        model = Task
        fields = ('id', 'user', 'title', 'due_date', 'timezone', 'note',
                    'notification_required', 'notification_time',
                    'is_editable', 'assigned_user_id')

    def to_representation(self, obj):
        result = {
            'id':obj.id,
            'user':obj.created_by.id,
            'title':obj.title,
            'due_date':obj.due_date.strftime("%m/%d/%Y %I:%M %p"),
            'timezone':obj.timezone,
            'note':obj.note,
            'notification_required':obj.notification_required,
            'notification_time':obj.notification_time,
            'is_editable':obj.is_editable,
            'created_by':obj.created_by.id,
            'created_by_first_name':obj.created_by.first_name,
            'created_by_last_name':obj.created_by.last_name
        }
        try:
            if self.assigned_user:
                result['assigned_user_id'] = self.assigned_user.id
                result['assigned_user_first_name'] = self.assigned_user.first_name
                result['assigned_user_last_name'] = self.assigned_user.last_name
        except:
            result['assigned_user_id'] = obj.user.id
            result['assigned_user_first_name'] = obj.user.first_name
            result['assigned_user_last_name'] = obj.user.last_name
        return result


    def validate(self, data):
        try:
            user = User.objects \
                    .filter(
                        Q(user_profiles__admin=data['user']) |
                        Q(user_profiles__admin__user_profiles__admin=data['user'])
                    ) \
                    .get(pk=data['assigned_user_id'])
        except:
            raise serializers.ValidationError("Assigned user doesn't exists.")
        else:
            self.assigned_user = user
        return data

    def create(self, validated_data):
        task = Task.objects.create(
            user=self.assigned_user,
            created_by=validated_data['user'],
            is_editable=validated_data['is_editable'],
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


class UserObject(object):
    def __init__(self, user=None, *args, **kwargs):
        if user:
            self.id = user.id
            if user.user_profiles.user_role == "super_admin":
                self.admin = user.id
                self.admin_first_name = user.first_name
                self.admin_last_name = user.last_name
            else:
                self.admin = user.user_profiles.admin.id
                self.admin_first_name = user.user_profiles.admin.first_name
                self.admin_last_name = user.user_profiles.admin.last_name
            self.first_name = user.first_name
            self.last_name = user.last_name
            self.email = user.email
            self.user_role = user.user_profiles.user_role
            self.is_active = user.is_active
            self.phone_number = user.user_profiles.phone_number
            self.address = user.user_profiles.address
            self.city = user.user_profiles.city
            self.state = user.user_profiles.state
            self.zip_code = user.user_profiles.zip_code
            self.country = user.user_profiles.country.name
            self.country_code = user.user_profiles.country.code
        else:
            self.admin = kwargs.get('admin', None)
            self.first_name = kwargs.get('first_name', None)
            self.last_name = kwargs.get('last_name', None)
            self.email = kwargs.get('email', None)
            self.user_role = kwargs.get('user_role', None)
            self.is_active = kwargs.get('is_active', None)
            self.phone_number = kwargs.get('phone_number', None)
            self.address = kwargs.get('address', None)
            self.city = kwargs.get('city', None)
            self.state = kwargs.get('state', None)
            self.zip_code = kwargs.get('zip_code', None)
            self.country = kwargs.get('country', None)


class UsersSerializer(serializers.Serializer):
    admin = serializers.IntegerField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    user_role = serializers.CharField()
    is_active = serializers.BooleanField()
    phone_number = serializers.CharField()
    address = serializers.CharField()
    city = serializers.CharField()
    state = serializers.CharField()
    zip_code = serializers.CharField()
    country = serializers.CharField()

    def to_representation(self, obj):
        data = UserObject(obj).__dict__
        return data

    def validate_email(self, value):
        if User.objects.filter(email=value).exists() and not self.instance:
            raise serializers.ValidationError("Email already exists.")
        return value

    def validate_admin(self, value):
        try:
            admin = User.objects.get(pk=value)
        except:
            pass
        else:
            if admin.user_profiles.user_role in ['super_admin','admin']:
                return admin
            else:
                raise serializers.ValidationError("Admin doesn't have required permissions.")
        raise serializers.ValidationError("Admin does not exists.")

    def create(self, validated_data):
        # generate password
        new_password = self._generate_password(10)

        # save user with password
        new_user = User(email=validated_data['email'], username=validated_data['email'])
        new_user.first_name = validated_data['first_name']
        new_user.last_name = validated_data['last_name']
        new_user.password = make_password(new_password)
        new_user.is_active = validated_data.get('is_active', False)
        new_user.save()
        self.user = new_user

        # save user profile
        new_token = self._generate_token()
        user_profile = UserProfiles(
            user = new_user,
            admin_status = 'enable',
            token = new_token,
            admin = validated_data['admin'],
            company_name = " ",
            occupation = " ",
            user_role = validated_data['user_role'],
            phone_number = validated_data['phone_number'],
            address = validated_data['address'],
            city = validated_data['city'],
            state = validated_data['state'],
            zip_code = validated_data['zip_code'],
            country = validated_data['country']
        )
        user_profile.save()

        # send password email with token
        url = '%s/accounts/login/%s/' % (settings.SERVER_URL, user_profile.token)
        message = 'Please login using this link %s with password %s' % (url, new_password)

        send_mail('Login Link', message, settings.EMAIL_HOST_USER,
            [str(new_user.email)], fail_silently=False)

        return new_user

    def update(self, instance, validated_data):
        # print "update", instance.user_profiles
        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.is_active = validated_data['is_active']
        instance.save()

        user_profile = instance.user_profiles
        user_profile.user_role = validated_data['user_role']
        user_profile.phone_number = validated_data['phone_number']
        user_profile.address = validated_data['address']
        user_profile.city = validated_data['city']
        user_profile.state = validated_data['state']
        user_profile.zip_code = validated_data['zip_code']
        user_profile.country = validated_data['country']
        user_profile.save()

        return instance

    def _generate_token(self):
        alphabet = [c for c in string.letters + string.digits if ord(c) < 128]
        return ''.join([random.choice(alphabet) for x in xrange(30)])

    def _generate_password(self, length):
        if not isinstance(length, int) or length < 8:
            raise ValueError("temp password must have positive length")

        chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
        return "".join([chars[ord(c) % len(chars)] for c in urandom(length)])
