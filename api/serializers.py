from rest_framework import serializers
from django.contrib.auth.models import User
from accounts.models import UserProfiles
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _

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