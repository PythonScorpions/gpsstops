from rest_framework import authentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from django.contrib.auth.models import User
from accounts.models import UserProfiles
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.contrib.sites.models import Site
from api.serializers import *


class CreateUser(APIView):

    # create a new user
    def post(self, request, *args, **kwargs):

        if User.objects.filter(email=request.data['email']):
            return Response({'code': 1, 'status': 200, 'message': 'Email Already Exist'})
        else:
            try:
                user_data = User(email=request.data['email'], username=request.data['email'],)
                user_data.first_name = request.data['name']
                user_data.password = make_password(request.data['password'])
                user_data.is_active = False
                user_data.save()
                user_profile_data = UserProfiles(user=user_data, address=request.data['address'],
                                                 city=request.data['city'], state=request.data['state'],
                                                 zip_code=request.data['zip_code'], country=request.data['country'],
                                                 phone_number=request.data['phone_number'],
                                                 occupation=request.data['occupation'],
                                                 company_name=request.data['company_name'])
                user_profile_data.save()
                message = 'Please verify your email by clicking on this link ' + 'http://gpsstops.pythonanywhere.com/verification/'+user_profile_data.token

                send_mail('Verification Link', message, 'scorpionspython@gmail.com', [str(user_data.email)],
                          fail_silently=False)
                return Response({'code': 0, 'status': 200, 'Data': 'Null', 'message': 'User has been created'})
            except:
                return Response({'code': 1, 'status': 200, 'message': 'All fields are mandatory'})


class UpdateUser(APIView):

    # create a new user
    def post(self, request, *args, **kwargs):

        user_id = self.kwargs['pk']

        if not User.objects.filter(id=int(user_id)):
            return Response({'code': 1, 'status': 200, 'message': 'User does not Exist'})
        else:
            try:
                user_data = User.objects.get(id=int(user_id))
                user_data.first_name = request.data['name']
                user_data.email = request.data['email']
                user_data.save()
                user_profile_data = UserProfiles.objects.get(user=user_data)
                user_profile_data.address = request.data['address']
                user_profile_data.city = request.data['city']
                user_profile_data.state = request.data['state']
                user_profile_data.zip_code = request.data['zip_code']
                user_profile_data.country = request.data['country']
                user_profile_data.phone_number = request.data['phone_number']
                user_profile_data.occupation = request.data['occupation']
                user_profile_data.company_name = request.data['company_name']

                user_profile_data.save()

                return Response({'code': 0, 'status': 200, 'Data': 'Null', 'message': 'User has been updated'})
            except:
                return Response({'code': 1, 'status': 200, 'message': 'All fields are mandatory'})


class LoginUser(APIView):

    def post(self, request, *args, **kwargs):

        email = request.data['email']
        password = request.data['password']
        user = authenticate(username=email, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return Response({'code': 0, 'status': 200, 'Data': {'user_id': request.user.id},
                                 'message': 'User is Logged In'})
            else:
                return Response({'code': 1, 'status': 200, 'Data': 'Null',
                                 'message': 'User has not verified Email'})
        else:
            return Response({'code': 1, 'status': 200, 'Data': 'Null',
                             'message': 'Wrong Credentials'})


class CurrentUser(APIView):

    def get(self, request, *args, **kwargs):

        user_id = self.kwargs['pk']
        try:
            user_data = User.objects.get(id=int(user_id))
            serializer = UserSerializer(user_data)
            profile_data = UserProfiles.objects.get(user=user_data)
            profile_serializer = UserProfileSerializer(profile_data)
            final_data = dict(serializer.data.items() + profile_serializer.data.items())
            final_data['name'] = user_data.first_name
            final_data['user_id'] = user_data.id
            return Response({'code': 0, 'status': 200, 'Data': final_data, 'message': 'current user details'})
        except:
            return Response({'code': 1, 'status': 200, 'message': 'User does not exist'})