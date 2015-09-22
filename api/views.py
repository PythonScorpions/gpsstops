'''
'''
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.contrib.sites.models import Site
from django.template import loader, RequestContext, Context
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django import forms
from django.conf import settings
from django.db.models import Q

from rest_framework import parsers, renderers, generics, authentication, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from appointments.models import *
from maps.models import *
from api.serializers import *
from accounts.models import *
from accounts.utils import *

from datetime import timedelta
import string, random, datetime, sys


for user in User.objects.all():
    Token.objects.get_or_create(user=user)


class CreateUser(APIView):

    # create a new user
    def post(self, request, *args, **kwargs):

        if User.objects.filter(email=request.data['email']):
            return Response({'code': 0, 'status': 200, 'message': 'Email Already Exist'})
        else:
            try:
                user_data = User(email=request.data['email'], username=request.data['email'],)
                user_data.first_name = request.data['name']
                user_data.password = make_password(request.data['password'])
                user_data.is_active = False
                user_data.save()
                user_profile_data = UserProfiles(
                    user=user_data, address=request.data['address'],
                    city=request.data['city'], state=request.data['state'],
                    zip_code=request.data['zip_code'], country=request.data['country'],
                    phone_number=request.data['phone_number'],
                    occupation=request.data['occupation'],
                    company_name=request.data['company_name'], admin_status='enable',
                    admin=user_data, user_role='super_admin')
                alphabet = [c for c in string.letters + string.digits if ord(c) < 128]
                user_profile_data.token = ''.join([random.choice(alphabet) for x in xrange(30)])
                user_profile_data.admin_status = 'enable'
                user_profile_data.save()

                url = '%s/verification/%s/' % (settings.SERVER_URL, user_profile_data.token)
                message = 'Please verify your email by clicking on this link %s' % (url,)

                send_mail('Verification Link', message, settings.EMAIL_HOST_USER,
                    [str(user_data.email)], fail_silently=False)
                return Response({'code': 1, 'status': 200, 'Data': 'Null', 'message': 'User has been created'})
            except:
                print sys.exc_info()
                try:
                    user_data.delete()
                    return Response({'code': 0, 'status': 200, 'message': 'All fields are mandatory'})
                except:
                    return Response({'code': 0, 'status': 200, 'message': 'All fields are mandatory'})


class UpdateUser(APIView):

    # create a new user
    def post(self, request, *args, **kwargs):

        user_id = self.kwargs['pk']

        if not User.objects.filter(id=int(user_id)):
            return Response({'code': 0, 'status': 200, 'message': 'User does not Exist'})
        else:
            try:
                user_data = User.objects.get(id=int(user_id))
                user_data.first_name = request.data['name']
                user_data.email = request.data['email']
                password = request.data.get('password', None)
                if password:
                    user_data.password = make_password(request.data['password'])
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

                return Response({'code': 1, 'status': 200, 'Data': 'Null', 'message': 'User has been updated'})
            except:
                print sys.exc_info()
                return Response({'code': 0, 'status': 200, 'message': 'All fields are mandatory'})


class LoginUser(APIView):

    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):

        email = request.data['username']
        password = request.data['password']
        user = authenticate(username=str(email), password=password)

        if user is not None:
            admin_status = UserProfiles.objects.get(user__email=str(email)).admin_status
            if admin_status == 'disabled':
                return Response({'code': 0, 'status': 200, 'Data': 'Null',
                                 'message': 'User is Disabled by Admin'})
            if user.is_active:
                return Response({'code': 1, 'status': 200, 'Data': {'user_id': request.user.id},
                                 'message': 'User is Logged In'})
            else:
                return Response({'code': 0, 'status': 200, 'Data': 'Null',
                                 'message': 'User has not verified Email'})
        else:
            return Response({'code': 0, 'status': 200, 'Data': 'Null',
                             'message': 'Wrong Credentials', 'ss': user})

class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)

    def post(self, request):
        # print "o"
        try:
            serializer = AuthTokenSerializer(data=request.data)
            serializer.is_valid()
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            profile_data = UserProfiles.objects.get(user=user).admin_status
            if profile_data == 'disabled':
                return Response({'code': 0, 'status': 200, 'Data': 'Null',
                                 'message': 'User has been disabled by admin'})
            if not user.is_active:
                return Response({'code': 0, 'status': 200, 'Data': 'Null',
                                 'message': 'Please verify your email'})

            return Response({'code': 1, 'status': 200, 'Data': {'user_id': user.id},
                             'message': 'User is Logged In'})
        except:
            return Response({'code': 0, 'status': 200, 'Data': 'Null',
                             'message': 'Wrong Credentials'})



class GetAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)

    def post(self, request):
        serializer = DeviceTokenSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)

            try:
                profile_data = UserProfiles.objects.get(user=user).admin_status
            except:
                print sys.exc_info()
            else:
                if profile_data == 'disabled':
                    return Response({'code': 0, 'status': 200, 'Data': 'Null',
                                     'message': 'User has been disabled by admin'})

                if not user.is_active:
                    return Response({'code': 0, 'status': 200, 'Data': 'Null',
                                     'message': 'Please verify your email'})

                RegistratedDevice.objects.get_or_create(
                    user=user,
                    device_token=serializer.validated_data['device_token'],
                    device_type=serializer.validated_data['device_type'],
                )
                return Response({'code': 1, 'status': 200,
                    'data': UserObject(user).__dict__, 'message': 'User is Logged In'})

        return Response({'code': 0, 'status': 200, 'Data': 'Null',
                             'message': 'Wrong Credentials'})


class CurrentUser(APIView):
    def get(self, request, *args, **kwargs):
        try:
            user = User.objects.get(pk=self.kwargs['pk'])
        except:
            pass
        else:
            data = UserObject(user).__dict__
            data['occupation'] = user.user_profiles.occupation
            data['company_name'] = user.user_profiles.company_name

            return Response({
                'code': 1,
                'status': 'success',
                'data': data,
                'message': 'current user details'
            })
        return Response({'code': 0, 'status': 'error', 'message': 'User does not exist'})

        # user_id = self.kwargs['pk']
        # try:
        #     user_data = User.objects.get(id=int(user_id))
        #     serializer = UserSerializer(user_data)
        #     profile_data = UserProfiles.objects.get(user=user_data)
        #     profile_serializer = UserProfileSerializer(profile_data)
        #     final_data = dict(serializer.data.items() + profile_serializer.data.items())
        #     final_data['name'] = user_data.first_name
        #     final_data['user_id'] = user_data.id

        #     return Response({'code': 1, 'status': 200, 'Data': final_data, 'message': 'current user details'})
        # except:
        #     return Response({'code': 0, 'status': 200, 'message': 'User does not exist'})


class LogoutUser(APIView):

    def post(self, request, *args, **kwargs):
        user_id = self.request.POST.get('user', None)
        device_token = self.request.POST.get('device_token', None)
        try:
            user = User.objects.get(id=int(user_id))
        except:
            return Response({'code': 0, 'status': 200, 'message': 'User does not exist'})

        try:
            RegistratedDevice.objects \
            .get(user=user, device_token=device_token) \
            .delete()
        except:
            return Response({'code': 0, 'status': 200, 'message': 'Device token doesn\'t exist'})
        else:
            return Response({'code': 1, 'status': 200, 'message': 'Logged out successfully'})


class CountryList(APIView):

    def get(self, request, *args, **kwargs):

        all_countries = [{'code': 'AD', 'name': 'Andorra'}, {'code': 'AF', 'name': 'Afghanistan'}, {'code': 'AG', 'name': 'Antigua and Barbuda'}, {'code': 'AL', 'name': 'Albania'}, {'code': 'AM', 'name': 'Armenia'}, {'code': 'AO', 'name': 'Angola'}, {'code': 'AR', 'name': 'Argentina'}, {'code': 'AT', 'name': 'Austria'}, {'code': 'AU', 'name': 'Australia'}, {'code': 'AZ', 'name': 'Azerbaijan'}, {'code': 'BB', 'name': 'Barbados'}, {'code': 'BD', 'name': 'Bangladesh'}, {'code': 'BE', 'name': 'Belgium'}, {'code': 'BF', 'name': 'Burkina Faso'}, {'code': 'BG', 'name': 'Bulgaria'}, {'code': 'BH', 'name': 'Bahrain'}, {'code': 'BI', 'name': 'Burundi'}, {'code': 'BJ', 'name': 'Benin'}, {'code': 'BN', 'name': 'Brunei Darussalam'}, {'code': 'BO', 'name': 'Bolivia'}, {'code': 'BR', 'name': 'Brazil'}, {'code': 'BS', 'name': 'Bahamas'}, {'code': 'BT', 'name': 'Bhutan'}, {'code': 'BW', 'name': 'Botswana'}, {'code': 'BY', 'name': 'Belarus'}, {'code': 'BZ', 'name': 'Belize'}, {'code': 'CA', 'name': 'Canada'}, {'code': 'CD', 'name': 'Democratic Republic of the Congo'}, {'code': 'CG', 'name': 'Republic of the Congo'}, {'code': 'CI', 'name': "C\xc3\xb4te d'Ivoire"}, {'code': 'CL', 'name': 'Chile'}, {'code': 'CM', 'name': 'Cameroon'}, {'code': 'CN', 'name': "People's Republic of China"}, {'code': 'CO', 'name': 'Colombia'}, {'code': 'CR', 'name': 'Costa Rica'}, {'code': 'CU', 'name': 'Cuba'}, {'code': 'CV', 'name': 'Cape Verde'}, {'code': 'CY', 'name': 'Cyprus'}, {'code': 'CZ', 'name': 'Czech Republic'}, {'code': 'DE', 'name': 'Germany'}, {'code': 'DJ', 'name': 'Djibouti'}, {'code': 'DK', 'name': 'Denmark'}, {'code': 'DM', 'name': 'Dominica'}, {'code': 'DO', 'name': 'Dominican Republic'}, {'code': 'EC', 'name': 'Ecuador'}, {'code': 'EE', 'name': 'Estonia'}, {'code': 'EG', 'name': 'Egypt'}, {'code': 'ER', 'name': 'Eritrea'}, {'code': 'ET', 'name': 'Ethiopia'}, {'code': 'FI', 'name': 'Finland'}, {'code': 'FJ', 'name': 'Fiji'}, {'code': 'FR', 'name': 'France'}, {'code': 'GA', 'name': 'Gabon'}, {'code': 'GE', 'name': 'Georgia'}, {'code': 'GH', 'name': 'Ghana'}, {'code': 'GM', 'name': 'The Gambia'}, {'code': 'GN', 'name': 'Guinea'}, {'code': 'GR', 'name': 'Greece'}, {'code': 'GT', 'name': 'Guatemala'}, {'code': 'GT', 'name': 'Haiti'}, {'code': 'GW', 'name': 'Guinea-Bissau'}, {'code': 'GY', 'name': 'Guyana'}, {'code': 'HN', 'name': 'Honduras'}, {'code': 'HU', 'name': 'Hungary'}, {'code': 'ID', 'name': 'Indonesia'}, {'code': 'IE', 'name': 'Republic of Ireland'}, {'code': 'IL', 'name': 'Israel'}, {'code': 'IN', 'name': 'India'}, {'code': 'IQ', 'name': 'Iraq'}, {'code': 'IR', 'name': 'Iran'}, {'code': 'IS', 'name': 'Iceland'}, {'code': 'IT', 'name': 'Italy'}, {'code': 'JM', 'name': 'Jamaica'}, {'code': 'JO', 'name': 'Jordan'}, {'code': 'JP', 'name': 'Japan'}, {'code': 'KE', 'name': 'Kenya'}, {'code': 'KG', 'name': 'Kyrgyzstan'}, {'code': 'KI', 'name': 'Kiribati'}, {'code': 'KP', 'name': 'North Korea'}, {'code': 'KR', 'name': 'South Korea'}, {'code': 'KW', 'name': 'Kuwait'}, {'code': 'LB', 'name': 'Lebanon'}, {'code': 'LI', 'name': 'Liechtenstein'}, {'code': 'LR', 'name': 'Liberia'}, {'code': 'LS', 'name': 'Lesotho'}, {'code': 'LT', 'name': 'Lithuania'}, {'code': 'LU', 'name': 'Luxembourg'}, {'code': 'LV', 'name': 'Latvia'}, {'code': 'LY', 'name': 'Libya'}, {'code': 'MG', 'name': 'Madagascar'}, {'code': 'MH', 'name': 'Marshall Islands'}, {'code': 'MK', 'name': 'Macedonia'}, {'code': 'ML', 'name': 'Mali'}, {'code': 'MM', 'name': 'Myanmar'}, {'code': 'MN', 'name': 'Mongolia'}, {'code': 'MR', 'name': 'Mauritania'}, {'code': 'MT', 'name': 'Malta'}, {'code': 'MU', 'name': 'Mauritius'}, {'code': 'MV', 'name': 'Maldives'}, {'code': 'MW', 'name': 'Malawi'}, {'code': 'MX', 'name': 'Mexico'}, {'code': 'MY', 'name': 'Malaysia'}, {'code': 'MZ', 'name': 'Mozambique'}, {'code': 'NA', 'name': 'Namibia'}, {'code': 'NE', 'name': 'Niger'}, {'code': 'NG', 'name': 'Nigeria'}, {'code': 'NI', 'name': 'Nicaragua'}, {'code': 'NL', 'name': 'Kingdom of the Netherlands'}, {'code': 'NO', 'name': 'Norway'}, {'code': 'NP', 'name': 'Nepal'}, {'code': 'NR', 'name': 'Nauru'}, {'code': 'NZ', 'name': 'New Zealand'}, {'code': 'OM', 'name': 'Oman'}, {'code': 'PA', 'name': 'Panama'}, {'code': 'PE', 'name': 'Peru'}, {'code': 'PG', 'name': 'Papua New Guinea'}, {'code': 'PH', 'name': 'Philippines'}, {'code': 'PK', 'name': 'Pakistan'}, {'code': 'PL', 'name': 'Poland'}, {'code': 'PT', 'name': 'Portugal'}, {'code': 'PW', 'name': 'Palau'}, {'code': 'PY', 'name': 'Paraguay'}, {'code': 'QA', 'name': 'Qatar'}, {'code': 'RO', 'name': 'Romania'}, {'code': 'RU', 'name': 'Russia'}, {'code': 'RW', 'name': 'Rwanda'}, {'code': 'SA', 'name': 'Saudi Arabia'}, {'code': 'SB', 'name': 'Solomon Islands'}, {'code': 'SC', 'name': 'Seychelles'}, {'code': 'SD', 'name': 'Sudan'}, {'code': 'SE', 'name': 'Sweden'}, {'code': 'SG', 'name': 'Singapore'}, {'code': 'SI', 'name': 'Slovenia'}, {'code': 'SK', 'name': 'Slovakia'}, {'code': 'SL', 'name': 'Sierra Leone'}, {'code': 'SM', 'name': 'San Marino'}, {'code': 'SN', 'name': 'Senegal'}, {'code': 'SO', 'name': 'Somalia'}, {'code': 'SR', 'name': 'Suriname'}, {'code': 'ST', 'name': 'S\xc3\xa3o Tom\xc3\xa9 and Pr\xc3\xadncipe'}, {'code': 'SY', 'name': 'Syria'}, {'code': 'TG', 'name': 'Togo'}, {'code': 'TH', 'name': 'Thailand'}, {'code': 'TJ', 'name': 'Tajikistan'}, {'code': 'TM', 'name': 'Turkmenistan'}, {'code': 'TN', 'name': 'Tunisia'}, {'code': 'TO', 'name': 'Tonga'}, {'code': 'TR', 'name': 'Turkey'}, {'code': 'TT', 'name': 'Trinidad and Tobago'}, {'code': 'TV', 'name': 'Tuvalu'}, {'code': 'TZ', 'name': 'Tanzania'}, {'code': 'UA', 'name': 'Ukraine'}, {'code': 'UG', 'name': 'Uganda'}, {'code': 'US', 'name': 'United States'}, {'code': 'UY', 'name': 'Uruguay'}, {'code': 'UZ', 'name': 'Uzbekistan'}, {'code': 'VA', 'name': 'Vatican City'}, {'code': 'VE', 'name': 'Venezuela'}, {'code': 'VN', 'name': 'Vietnam'}, {'code': 'VU', 'name': 'Vanuatu'}, {'code': 'YE', 'name': 'Yemen'}, {'code': 'ZM', 'name': 'Zambia'}, {'code': 'ZW', 'name': 'Zimbabwe'}, {'code': 'DZ', 'name': 'Algeria'}, {'code': 'BA', 'name': 'Bosnia and Herzegovina'}, {'code': 'KH', 'name': 'Cambodia'}, {'code': 'CF', 'name': 'Central African Republic'}, {'code': 'TD', 'name': 'Chad'}, {'code': 'KM', 'name': 'Comoros'}, {'code': 'HR', 'name': 'Croatia'}, {'code': 'TL', 'name': 'East Timor'}, {'code': 'SV', 'name': 'El Salvador'}, {'code': 'GQ', 'name': 'Equatorial Guinea'}, {'code': 'GD', 'name': 'Grenada'}, {'code': 'KZ', 'name': 'Kazakhstan'}, {'code': 'LA', 'name': 'Laos'}, {'code': 'FM', 'name': 'Federated States of Micronesia'}, {'code': 'MD', 'name': 'Moldova'}, {'code': 'MC', 'name': 'Monaco'}, {'code': 'ME', 'name': 'Montenegro'}, {'code': 'MA', 'name': 'Morocco'}, {'code': 'KN', 'name': 'Saint Kitts and Nevis'}, {'code': 'LC', 'name': 'Saint Lucia'}, {'code': 'VC', 'name': 'Saint Vincent and the Grenadines'}, {'code': 'WS', 'name': 'Samoa'}, {'code': 'RS', 'name': 'Serbia'}, {'code': 'ZA', 'name': 'South Africa'}, {'code': 'ES', 'name': 'Spain'}, {'code': 'LK', 'name': 'Sri Lanka'}, {'code': 'SZ', 'name': 'Swaziland'}, {'code': 'CH', 'name': 'Switzerland'}, {'code': 'AE', 'name': 'United Arab Emirates'}, {'code': 'GB', 'name': 'United Kingdom'}]

        return Response(all_countries)


class ForgotPassword(APIView):

    def post(self, request, *args, **kwargs):

        user_email = request.data['email']
        if User.objects.filter(email=user_email).exists():
            email = User.objects.get(email=request.POST['email'])
            user = UserProfiles.objects.get(user=email)

            site = settings.SERVER_URL
            t = loader.get_template('password.txt')
            c = Context({
                    'name': email.first_name,
                    'email': email,
                    'site': site.name,
                    'token': user.token
                })

            send_mail(
                '[%s] %s' % (site, 'New Contactus Request'),
                t.render(c),
                settings.EMAIL_HOST_USER,
                [email.email],
                fail_silently=False
            )
            return Response({'code': 1, 'status': 200, 'Data': 'Null', 'message': 'Email has been sent'})
        else:
            return Response({'code': 0, 'status': 200, 'message': 'User does not exist'})


class CreateRouteApi(APIView):

    def _format_distance(self, request, key):
        if '.' in request.data[key]:
            distance = float(request.data[key][:-3])
        else:
            distance = float(int(request.data[key][:-3]))
        return distance

    def _set_data(self, request):
        self.is_editable = request.data['is_editable']
        self.trip_title = request.data['trip_title']

        trip_datetime_str = str(request.data['trip_datetime'])
        self.trip_datetime = datetime.datetime.strptime(
                                trip_datetime_str, "%Y/%m/%d %H:%M")

        self.total_time = request.data['total_hours']
        self.optimized_total_time = request.data['optimized_total_hours']
        self.total_distance = self._format_distance(request, 'total_distance')
        self.optimized_total_distance = self._format_distance(request, 'optimized_total_distance')
        # print self.trip_title
        # print type(self.trip_datetime), "-----------------", self.trip_datetime

    def _create_route(self):
        route_obj = Route(
            user=self.assigned_user,
            trip_title=self.trip_title,
            trip_datetime=self.trip_datetime,
            total_distance=self.total_distance,
            total_time=self.total_time,
            optimized_total_time=self.optimized_total_time,
            optimized_total_distance=self.optimized_total_distance,
            created_by=self.user_obj,
            is_editable=True if self.is_editable == 1 or self.is_editable == "1" else False
        )
        route_obj.save()
        return route_obj

    def _set_user(self, request):
        try:
            self.user_obj = User.objects.get(id=int(request.data['user_id']))
        except:
            pass
        else:
            return self.user_obj
        return None

    def _set_assigned_user(self, request):
        try:
            self.assigned_user = User.objects \
                                 .get(pk=int(request.data['assigned_user_id']))
        except:
            pass
        else:
            return self.assigned_user
        return None

    def _save_locations(self, request):
        for idx, loc in enumerate(request.data['location']):
            if loc['latitude'] and loc['longitude']:
                loc_obj = Location(
                    route=self.route_obj,
                    location_address=loc['location_name'],
                    location_near_address=loc['near_by_location'],
                    location_lat=loc['latitude'],
                    location_long=loc['longitude'],
                    location_note=loc['note'],
                    distance=loc['distance'],
                    time=loc['time']
                )

                if idx == 0:
                    loc_obj.location_number = 11
                    loc_obj.save()
                elif idx == len(request.data['location'])-1:
                    loc_obj.location_number = 22
                    loc_obj.save()
                else:
                    loc_obj.location_number = idx
                    loc_obj.save()
            else:
                pass

    def _save_optimized_locations(self, request):
        for idx, loc in enumerate(request.data['optimized_location']):
            if loc['latitude'] and loc['longitude']:
                loc_obj = OptimizedLocation(
                    route=self.route_obj,
                    location_address=loc['location_name'],
                    location_near_address=loc['near_by_location'],
                    location_lat=loc['latitude'],
                    location_long=loc['longitude'],
                    location_note=loc['note'],
                    distance=loc['distance'],
                    time=loc['time']
                )
                if idx == 0:
                    loc_obj.location_number = 11
                    loc_obj.save()
                elif idx == len(request.data['location'])-1:
                    loc_obj.location_number = 22
                    loc_obj.save()
                else:
                    loc_obj.location_number = idx
                    loc_obj.save()
            else:
                pass

    # @staticmethod
    def post(self, request):
        self._set_data(request)

        if not self._set_user(request):
            return Response({'code': 0, 'status': 200,
                'message': 'User does not exist'})

        if not self._set_assigned_user(request):
            return Response({'code': 0, 'status': 200,
                'message': 'Assigned User does not exist'})

        self.route_obj = self._create_route()
        self._save_locations(request)
        self._save_optimized_locations(request)

        return Response({'code': 1, 'status': 200, 'Data': 'Null',
            'message': 'Route has been created'})


class RouteListApi(APIView):
    def get(self, request, *args, **kwargs):
        try:
            user_id = int(self.kwargs['pk'])
            user = User.objects.get(pk=user_id)
        except:
            return Response({
                'code':0,
                'status':200,
                'message':'User does not exist'
            })

        # routes = Route.objects.filter(user__id=user_id)
        routes = filter_objects_by_user(user, Route)
        serializer = RouteSerializer(routes, many=True)
        return Response({
            'code':1,
            'status':200,
            'Data':serializer.data,
            'message':'All routes Data'
        })


class OptimizedRouteListApi(APIView):

    def get(self, request, *args, **kwargs):
        try:
            user_id = int(self.kwargs['pk'])
            user = User.objects.get(pk=user_id)
        except:
            return Response({'code': 0, 'status': 200, 'message': 'User does not exist'})

        # routes = Route.objects.filter(user__id=user_id)
        routes = filter_objects_by_user(user, Route)
        serializer = OptRouteSerializer(routes, many=True)

        return Response({'code': 1, 'status': 200, 'Data': serializer.data, 'message': 'All routes Data'})


class EditRouteApi(APIView):

    def _get_route(self):
        try:
            self.route_obj = Route.objects.get(id=int(self.kwargs['pk']))
        except:
            pass
        else:
            return self.route_obj
        return None

    def _format_distance(self, request, key):
        if '.' in request.data[key]:
            distance = float(request.data[key][:-3])
        else:
            distance = float(int(request.data[key][:-3]))
        return distance

    def _set_data(self, request):
        self.is_editable = request.data['is_editable']
        self.trip_title = request.data['trip_title']

        trip_datetime_str = str(request.data['trip_datetime'])
        self.trip_datetime = datetime.datetime.strptime(
                                trip_datetime_str, "%Y/%m/%d %H:%M")

        self.total_time = request.data['total_hours']
        self.optimized_total_time = request.data['optimized_total_hours']
        self.total_distance = self._format_distance(request, 'total_distance')
        self.optimized_total_distance = self._format_distance(request, 'optimized_total_distance')

    def _set_user(self, request):
        try:
            self.user_obj = User.objects.get(id=int(request.data['user_id']))
        except:
            pass
        else:
            return self.user_obj
        return None

    def _set_assigned_user(self, request):
        try:
            self.assigned_user = User.objects \
                                 .get(pk=int(request.data['assigned_user_id']))
        except:
            pass
        else:
            return self.assigned_user
        return None

    def _save_route(self):
        self.route_obj.user = self.assigned_user
        self.route_obj.created_by = self.user_obj
        self.route_obj.is_editable = self.is_editable

        self.route_obj.trip_title = self.trip_title
        self.route_obj.trip_datetime = self.trip_datetime
        self.route_obj.total_distance = self.total_distance
        self.route_obj.total_time = self.total_time
        self.route_obj.optimized_total_distance = self.optimized_total_distance
        self.route_obj.optimized_total_time = self.optimized_total_time

        self.route_obj.save()

    def _save_locations(self, request):
        for idx, loc in enumerate(request.data['location']):
            if loc['latitude'] and loc['longitude']:
                loc_obj = Location(
                    route=self.route_obj,
                    location_address=loc['location_name'],
                    location_near_address=loc['near_by_location'],
                    location_lat=loc['latitude'],
                    location_long=loc['longitude'],
                    location_note=loc['note'],
                    distance=loc['distance'],
                    time=loc['time']
                )

                if idx == 0:
                    loc_obj.location_number = 11
                    loc_obj.save()
                elif idx == len(request.data['location'])-1:
                    loc_obj.location_number = 22
                    loc_obj.save()
                else:
                    loc_obj.location_number = idx
                    loc_obj.save()
            else:
                pass

    def _save_optimized_locations(self, request):
        for idx, loc in enumerate(request.data['optimized_location']):
            if loc['latitude'] and loc['longitude']:
                loc_obj = OptimizedLocation(
                    route=self.route_obj,
                    location_address=loc['location_name'],
                    location_near_address=loc['near_by_location'],
                    location_lat=loc['latitude'],
                    location_long=loc['longitude'],
                    location_note=loc['note'],
                    distance=loc['distance'],
                    time=loc['time']
                )
                if idx == 0:
                    loc_obj.location_number = 11
                    loc_obj.save()
                elif idx == len(request.data['location'])-1:
                    loc_obj.location_number = 22
                    loc_obj.save()
                else:
                    loc_obj.location_number = idx
                    loc_obj.save()
            else:
                pass

    def get(self, request, *args, **kwargs):
        try:
            route_id = int(self.kwargs['pk'])
            route_obj = Route.objects.get(id=route_id)
        except:
            return Response({'code': 0, 'status': 200,
                'message': 'Route does not exist'})

        route_serializer = RouteSerializer(route_obj)
        return Response({'code': 1, 'status': 200,
            'Data': route_serializer.data, 'message': 'All routes Data'})

    def post(self, request, *args, **kwargs):
        if not self._get_route():
            return Response({'code':0, 'status':200,
                'message':'Route does not exist'})

        if not self._set_user(request):
            return Response({'code':0, 'status':200,
                'message':'User does not exist'})

        if not self._set_assigned_user(request):
            return Response({'code':0, 'status':200,
                'message':'Assigned user does not exist'})

        self._set_data(request)
        self._save_route()

        try:
            Location.objects.filter(route=self.route_obj).delete()
            OptimizedLocation.objects.filter(route=self.route_obj).delete()

            self._save_locations(request)
            self._save_optimized_locations(request)
        except:
            return Response({'code':0, 'status':200, 'message':'Something went wrong'})

        return Response({'code':1, 'status':200, 'Data':'Null', 'message':'Route has been updated'})


class OptimizedEditRouteApi(APIView):

    def get(self, request, *args, **kwargs):
        try:
            route_id = int(self.kwargs['pk'])
            route_obj = Route.objects.get(id=route_id)
        except:
            return Response({'code': 0, 'status': 200, 'message': 'Route does not exist'})
        route_serializer = OptRouteSerializer(route_obj)
        return Response({'code': 1, 'status': 200, 'Data': route_serializer.data, 'message': 'All routes Data'})


class Events(APIView):

    def _get_objects(self, user, model_class):
        if user.user_profiles.user_role == "super_admin":
            objects = model_class.objects \
                        .filter(
                            Q(user=user) |
                            Q(user__user_profiles__admin=user) |
                            Q(user__user_profiles__admin__user_profiles__admin=user)
                        )
        elif user.user_profiles.user_role == "admin":
            objects = model_class.objects \
                        .filter(
                            Q(user=user) |
                            Q(user__user_profiles__admin=user) |
                            Q(user__user_profiles__admin=user.user_profiles.admin)
                        )
        else:
            objects = model_class.objects.filter(user=user)
        return objects

    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        events = []

        routes = self._get_objects(request.user, Route)
        for idx, rou in enumerate(routes):
            temp = dict()
            temp['id'] = str(rou.id)
            title = ''
            locations = Location.objects.filter(route=rou).order_by('id')
            for index, loc in enumerate(locations):
                if index == 0:
                    title += loc.location_address.split(' ')[0][:-1]
                else:
                    title += '-'
                    title += loc.location_address.split(' ')[0][:-1]
            temp['title'] = title
            temp['locations_count'] = locations.count()
            temp['distance'] = rou.total_distance
            temp['time'] = rou.total_time
            temp['trip_title'] = rou.trip_title
            temp['trip_datetime'] = rou.trip_datetime
            temp['url'] = '/maps/edit_route/' + str(rou.id)
            temp['class'] = 'event-info'
            temp['start'] = str((int(rou.trip_datetime.strftime("%s")) * 1000)-19800000)
            if rou.total_time[1] == ' ':
                add_hour = int(rou.total_time[:1])
            else:
                add_hour = int(rou.total_time[:2])
            if rou.total_time[7:9]:
                add_minute = int(rou.total_time[7:9])
            else:
                add_minute = 0
            add_time = rou.trip_datetime + timedelta(minutes=add_minute, hours=add_hour)
            temp['end'] = str((int(add_time.strftime("%s")) * 1000)-19800000)
            temp['route'] = 'true'
            events.append(temp)

        appointments = self._get_objects(request.user, Appointments)
        for appointment in appointments:
            temp = {}
            temp['id'] = appointment.id
            temp['title'] = appointment.title
            temp['url'] = '/appointments/%s/' % appointment.id
            temp['class'] = 'event-warning appointment'
            temp['start'] = str((int(appointment.start_datetime.strftime("%s")) * 1000)-19800000)
            temp['appointment'] = 'true'
            events.append(temp)


        tasks = self._get_objects(request.user, Task)
        for task in tasks:
            temp = {}
            temp['id'] = task.id
            temp['title'] = task.title
            temp['url'] = '/appointments/task/%s/' % task.id
            temp['class'] = 'event-success task'
            if task.due_date:
                temp['start'] = str((int(task.due_date.strftime("%s")) * 1000)-19800000)
            temp['task'] = 'true'
            events.append(temp)

        return Response({'success': 1, 'result': events})


class DeleteRouteApi(APIView):

    def post(self, request, *args, **kwargs):
        try:
            route_id = int(self.kwargs['pk'])
            route_obj = Route.objects.get(id=route_id)
            route_obj.delete()
            return Response({'code': 1, 'status': 200, 'Data': 'Null', 'message': 'Route has been deleted'})
        except:
            return Response({'code': 0, 'status': 200, 'message': 'Route with this id does not exist'})


class RoutesPerDay(APIView):

    def get(self, request, *args, **kwargs):
        try:
            user_id = int(self.kwargs['pk'])
            user = User.objects.get(pk=user_id)
        except:
            return Response({'code': 0, 'status': 200, 'message': 'User does not exist'})
        year = int(self.kwargs['year'])
        month = int(self.kwargs['month'])
        day = int(self.kwargs['day'])
        date_selected = datetime.date(year, month, day)

        # routes = Route.objects.filter(user__id=user_id, trip_datetime__startswith=date_selected)
        routes = filter_objects_by_user(user, Route) \
                 .filter(trip_datetime__startswith=date_selected)
        serializer = RouteSerializer(routes, many=True)

        return Response({'code': 1, 'status': 200, 'Data': serializer.data, 'message': 'Datewise routes Data'})


class QueryForm(forms.Form):
    date = forms.DateField(required=False)
    user = forms.IntegerField()


class AppointmentsViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentsSerializer

    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.request.method == 'GET':
            form = QueryForm(self.request.query_params)
        else:
            form = QueryForm(self.request.data)

        if form.is_valid():
            user = form.cleaned_data.get('user',0)
            date = form.cleaned_data.get('date', None)

            try:
                user_obj = User.objects.get(pk=user)
            except:
                pass
            else:
                appointments = filter_objects_by_user(user_obj, Appointments)
                # appointments = Appointments.objects.filter(user__id=user)
                if date and self.request.method == 'GET':
                    min_date = datetime.datetime.combine(date, datetime.datetime.min.time())
                    max_date = datetime.datetime.combine(date, datetime.datetime.max.time())
                    appointments = appointments \
                                    .filter(start_datetime__gte=min_date,
                                        start_datetime__lte=max_date)
                return appointments
        return Appointments.objects.none()

    def dispatch(self, request, *args, **kwargs):
        super(AppointmentsViewSet, self).dispatch(request, *args, **kwargs)
        if self.response.status_code in [200, 201, 202, 204]:
            code = 1
            message = 'success'
        elif self.response.status_code == 400:
            code = 0
            message = 'Invalid input'
        elif self.response.status_code == 401:
            code = 0
            message = 'Unauthorized Access'
        elif self.response.status_code == 404:
            code = 0
            message = 'API not found'
        else:
            code = 0
            message = 'Some error occurred'

        self.response.data = {
            'code': code,
            'message': message,
            'data': self.response.data
        }

        self.response.status_code = 200
        self.response.render()
        return self.response


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer

    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.request.method == 'GET':
            form = QueryForm(self.request.query_params)
        else:
            form = QueryForm(self.request.data)

        if form.is_valid():
            user = form.cleaned_data.get('user',0)
            date = form.cleaned_data.get('date', None)

            try:
                user_obj = User.objects.get(pk=user)
            except:
                pass
            else:
                tasks = filter_objects_by_user(user_obj, Task)
                # tasks = Task.objects.filter(user__id=user)
                if date and self.request.method == 'GET':
                    min_date = datetime.datetime.combine(date, datetime.datetime.min.time())
                    max_date = datetime.datetime.combine(date, datetime.datetime.max.time())
                    tasks = tasks \
                            .filter(due_date__gte=min_date,
                                due_date__lte=max_date)
                return tasks
        return Task.objects.none()

    def dispatch(self, request, *args, **kwargs):
        super(TaskViewSet, self).dispatch(request, *args, **kwargs)
        if self.response.status_code in [200, 201, 202, 204]:
            code = 1
            message = 'success'
        elif self.response.status_code == 400:
            code = 0
            message = 'Invalid input'
        elif self.response.status_code == 401:
            code = 0
            message = 'Unauthorized Access'
        elif self.response.status_code == 404:
            code = 0
            message = 'API not found'
        else:
            code = 0
            message = 'Some error occurred'

        self.response.data = {
            'code': code,
            'message': message,
            'data': self.response.data
        }
        self.response.status_code = 200
        self.response.render()
        return self.response


class ContactViewSet(viewsets.ModelViewSet):
    serializer_class = ContactSerializer

    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.request.method == 'GET':
            form = QueryForm(self.request.query_params)
        else:
            form = QueryForm(self.request.data)

        if form.is_valid():
            user = form.cleaned_data.get('user',0)
            return Contacts.objects.filter(user__id=user)
        return Contacts.objects.none()

    def list(self, request):
        response = super(ContactViewSet, self).list(request)
        queryset = self.get_queryset()
        for i in range(queryset.count()):
            if queryset[i].group:
                response.data[i]['group_name'] = queryset[i].group.name
            else:
                response.data[i]['group_name'] = ""
        return response

    def dispatch(self, request, *args, **kwargs):
        super(ContactViewSet, self).dispatch(request, *args, **kwargs)
        if self.response.status_code in [200, 201, 202, 204]:
            code = 1
            message = 'success'
        elif self.response.status_code == 400:
            code = 0
            message = 'Invalid input'
        elif self.response.status_code == 401:
            code = 0
            message = 'Unauthorized Access'
        elif self.response.status_code == 404:
            code = 0
            message = 'API not found'
        else:
            code = 0
            message = 'Some error occurred'

        self.response.data = {
            'code': code,
            'message': message,
            'data': self.response.data
        }
        self.response.status_code = 200
        self.response.render()
        return self.response


class ContactGroupViewSet(viewsets.ModelViewSet):
    serializer_class = ContactGroupSerializer

    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.request.method == 'GET':
            form = QueryForm(self.request.query_params)
        else:
            form = QueryForm(self.request.data)

        if form.is_valid():
            user = form.cleaned_data.get('user',0)
            return ContactGroup.objects.filter(user__id=user)
        return ContactGroup.objects.none()

    def dispatch(self, request, *args, **kwargs):
        super(ContactGroupViewSet, self).dispatch(request, *args, **kwargs)
        if self.response.status_code in [200, 201, 202, 204]:
            code = 1
            message = 'success'
        elif self.response.status_code == 400:
            code = 0
            message = 'Invalid input'
        elif self.response.status_code == 401:
            code = 0
            message = 'Unauthorized Access'
        elif self.response.status_code == 404:
            code = 0
            message = 'API not found'
        else:
            code = 0
            message = 'Some error occurred'

        self.response.data = {
            'code': code,
            'message': message,
            'data': self.response.data
        }
        self.response.status_code = 200
        self.response.render()
        return self.response


class AgendaView(APIView):
    def get(self, request, *args, **kwargs):
        form = QueryForm(self.request.query_params)

        if form.is_valid():
            user = form.cleaned_data.get('user',0)
            given_date = form.cleaned_data.get('date', None)

            if not given_date:
                return Response({'code':0, 'status':'error',
                            'message':'Invalid date format.'})

            agenda = []

            appointments = Appointments.objects \
                            .filter(user=user) \
                            .filter(start_datetime__gte=given_date)
            for appointment in appointments:
                agenda.append({
                    'id':appointment.id,
                    'title':appointment.title,
                    'date':appointment.start_datetime.date(),
                    'type':'appointments'
                })

            tasks = Task.objects \
                      .filter(user=user) \
                      .filter(due_date__gte=given_date)
            for task in tasks:
                agenda.append({
                    'id':task.id,
                    'title':task.title,
                    'date':task.due_date.date(),
                    'type':'task'
                })

            return Response({'code': 1, 'status': 200, 'data':agenda})
        else:
            return Response({'code':0, 'status':'error', 'message':form.errors})


class UsersViewSet(viewsets.ViewSet):

    def list(self, request):
        try:
            user = User.objects.get(pk=request.query_params.get('user'))
        except:
            pass
        else:
            queryset = get_users(user)
            if request.query_params.get('admin_only') == "1":
                queryset = queryset.filter(user_profiles__user_role='admin')
            serializer = UsersSerializer(queryset, many=True)
            return Response({'code':1, 'status':'success', 'data':serializer.data})
        return Response({'code':0, 'status':'error', 'data':'Invalid user id.'})

    def retrieve(self, request, pk=None):
        try:
            admin = User.objects.get(pk=request.query_params['admin'])
        except:
            return Response({'code':0, 'status':'error', 'data':'Invalid admin user id.'})

        users = get_users(admin)
        try:
            user = users.get(pk=pk)
        except:
            pass
        else:
            data = UserObject(user).__dict__
            return Response({'code':1, 'status':'success', 'data':data})
        return Response({'code':0, 'status':'error', 'data':'Invalid user id.'})

    def create(self, request):
        serializer = UsersSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            data['id'] = serializer.user.id
            return Response({'code':1, 'status':'success', 'data':data})
        else:
            print serializer.errors
            return Response({'code':0, 'status':'error', 'data':serializer.errors})

    def update(self, request, pk=None):
        try:
            admin = User.objects.get(pk=request.data.get('admin'))
        except:
            return Response({'code':0, 'status':'error', 'data':'Invalid admin user id.'})

        users = get_users(admin)
        print users
        try:
            user = users.get(pk=pk)
        except:
            print sys.exc_info();
            pass
        else:
            serializer = UsersSerializer(data=request.data, instance=user)
            if serializer.is_valid():
                serializer.save()
                data = serializer.data
                data['id'] = user.id
                return Response({'code':1, 'status':'success', 'data':data})
            else:
                return Response({'code':0, 'status':'error', 'data':serializer.errors})
        return Response({'code':0, 'status':'error', 'data':'Invalid user id.'})

    @detail_route(methods=['post'])
    def change_status(self, request, pk=None):
        try:
            admin = User.objects.get(pk=request.POST.get('admin'))
        except:
            return Response({'code':0, 'status':'error', 'data':'Invalid admin user id.'})

        users = get_users(admin)
        try:
            user = users.get(pk=pk)
        except:
            pass
        else:
            try:
                status = int(request.POST.get('is_active', -1))
            except:
                status = -1

            if status == 0:
                user.is_active = False
                user.save()
            elif status == 1:
                user.is_active = True
                user.save()
            else:
                return Response({'code':0, 'status':'error', 'data':'Value of is_active is invalid.'})

            data = UserObject(user).__dict__
            return Response({'code':1, 'status':'success', 'data':data})
        return Response({'code':0, 'status':'error', 'data':'Invalid user id.'})


class ThemeView(APIView):
    def get(self, request, *args, **kwargs):
        form = QueryForm(self.request.query_params)

        if form.is_valid():
            user_id = form.cleaned_data.get('user',0)

            try:
                user = User.objects.get(pk=user_id)
            except:
                return Response({'code':0, 'status':'error',
                    'message':'User not found.'})

            try:
                if user.user_profiles.user_role == "super_admin":
                    organization = Organization.objects.get(super_admin=user)
                elif user.user_profiles.user_role == "admin":
                    organization = Organization.objects.get(admin=user)
                elif user.user_profiles.user_role == "employee":
                    organization = Organization.objects.get(employees=user)
            except:
                organization = None

            if not organization:
                return Response({'code':0, 'status':'error',
                    'message':'No matching organization'})

            if organization.theme:
                return Response({
                    'code': 1, 'status': 200,
                    'active_button_color':organization.theme.active_button_color,
                    'background_color':organization.theme.background_color,
                    'inactive_button_color':organization.theme.inactive_button_color,
                    'logo_url':"http://bennyapp.com/media/" + organization.theme.logo.name if organization.theme.logo else '',
                    'navigation_color':organization.theme.navigation_color,
                    'active_button_text_color':organization.theme.active_button_text_color,
                    'inactive_button_text_color':organization.theme.inactive_button_text_color
                })
            else:
                return Response({'code':0, 'status':'error',
                    'message':'No theme set yet.'})
        else:
            return Response({'code':0, 'status':'error', 'message':form.errors})
