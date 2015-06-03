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
from rest_framework.authtoken.models import Token
from rest_framework import parsers
from rest_framework import renderers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.template import loader
from django.template import RequestContext, Context
import string
import random


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
                user_profile_data = UserProfiles(user=user_data, address=request.data['address'],
                                                 city=request.data['city'], state=request.data['state'],
                                                 zip_code=request.data['zip_code'], country=request.data['country'],
                                                 phone_number=request.data['phone_number'],
                                                 occupation=request.data['occupation'],
                                                 company_name=request.data['company_name'])
                alphabet = [c for c in string.letters + string.digits if ord(c) < 128]
                user_profile_data.token = ''.join([random.choice(alphabet) for x in xrange(30)])
                user_profile_data.save()
                message = 'Please verify your email by clicking on this link ' + 'http://gpsstops.pythonanywhere.com/verification/'+user_profile_data.token

                send_mail('Verification Link', message, 'scorpionspython@gmail.com', [str(user_data.email)],
                          fail_silently=False)
                return Response({'code': 1, 'status': 200, 'Data': 'Null', 'message': 'User has been created'})
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
                return Response({'code': 0, 'status': 200, 'message': 'All fields are mandatory'})


class LoginUser(APIView):

    def post(self, request, *args, **kwargs):

        email = request.data['email']
        password = request.data['password']
        user = authenticate(username=email, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return Response({'code': 1, 'status': 200, 'Data': {'user_id': request.user.id},
                                 'message': 'User is Logged In'})
            else:
                return Response({'code': 0, 'status': 200, 'Data': 'Null',
                                 'message': 'User has not verified Email'})
        else:
            return Response({'code': 0, 'status': 200, 'Data': 'Null',
                             'message': 'Wrong Credentials'})

class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)

    def post(self, request):
        print "o"
        try:
            serializer = AuthTokenSerializer(data=request.data)
            serializer.is_valid()
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({'code': 1, 'status': 200, 'Data': {'user_id': user.id},
                             'message': 'User is Logged In'})
        except:
            return Response({'code': 0, 'status': 200, 'Data': 'Null',
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
            return Response({'code': 1, 'status': 200, 'Data': final_data, 'message': 'current user details'})
        except:
            return Response({'code': 0, 'status': 200, 'message': 'User does not exist'})


class CountryList(APIView):

    def get(self, request, *args, **kwargs):

        all_countries = [{'code': 'AD', 'name': 'Andorra'}, {'code': 'AF', 'name': 'Afghanistan'}, {'code': 'AG', 'name': 'Antigua and Barbuda'}, {'code': 'AL', 'name': 'Albania'}, {'code': 'AM', 'name': 'Armenia'}, {'code': 'AO', 'name': 'Angola'}, {'code': 'AR', 'name': 'Argentina'}, {'code': 'AT', 'name': 'Austria'}, {'code': 'AU', 'name': 'Australia'}, {'code': 'AZ', 'name': 'Azerbaijan'}, {'code': 'BB', 'name': 'Barbados'}, {'code': 'BD', 'name': 'Bangladesh'}, {'code': 'BE', 'name': 'Belgium'}, {'code': 'BF', 'name': 'Burkina Faso'}, {'code': 'BG', 'name': 'Bulgaria'}, {'code': 'BH', 'name': 'Bahrain'}, {'code': 'BI', 'name': 'Burundi'}, {'code': 'BJ', 'name': 'Benin'}, {'code': 'BN', 'name': 'Brunei Darussalam'}, {'code': 'BO', 'name': 'Bolivia'}, {'code': 'BR', 'name': 'Brazil'}, {'code': 'BS', 'name': 'Bahamas'}, {'code': 'BT', 'name': 'Bhutan'}, {'code': 'BW', 'name': 'Botswana'}, {'code': 'BY', 'name': 'Belarus'}, {'code': 'BZ', 'name': 'Belize'}, {'code': 'CA', 'name': 'Canada'}, {'code': 'CD', 'name': 'Democratic Republic of the Congo'}, {'code': 'CG', 'name': 'Republic of the Congo'}, {'code': 'CI', 'name': "C\xc3\xb4te d'Ivoire"}, {'code': 'CL', 'name': 'Chile'}, {'code': 'CM', 'name': 'Cameroon'}, {'code': 'CN', 'name': "People's Republic of China"}, {'code': 'CO', 'name': 'Colombia'}, {'code': 'CR', 'name': 'Costa Rica'}, {'code': 'CU', 'name': 'Cuba'}, {'code': 'CV', 'name': 'Cape Verde'}, {'code': 'CY', 'name': 'Cyprus'}, {'code': 'CZ', 'name': 'Czech Republic'}, {'code': 'DE', 'name': 'Germany'}, {'code': 'DJ', 'name': 'Djibouti'}, {'code': 'DK', 'name': 'Denmark'}, {'code': 'DM', 'name': 'Dominica'}, {'code': 'DO', 'name': 'Dominican Republic'}, {'code': 'EC', 'name': 'Ecuador'}, {'code': 'EE', 'name': 'Estonia'}, {'code': 'EG', 'name': 'Egypt'}, {'code': 'ER', 'name': 'Eritrea'}, {'code': 'ET', 'name': 'Ethiopia'}, {'code': 'FI', 'name': 'Finland'}, {'code': 'FJ', 'name': 'Fiji'}, {'code': 'FR', 'name': 'France'}, {'code': 'GA', 'name': 'Gabon'}, {'code': 'GE', 'name': 'Georgia'}, {'code': 'GH', 'name': 'Ghana'}, {'code': 'GM', 'name': 'The Gambia'}, {'code': 'GN', 'name': 'Guinea'}, {'code': 'GR', 'name': 'Greece'}, {'code': 'GT', 'name': 'Guatemala'}, {'code': 'GT', 'name': 'Haiti'}, {'code': 'GW', 'name': 'Guinea-Bissau'}, {'code': 'GY', 'name': 'Guyana'}, {'code': 'HN', 'name': 'Honduras'}, {'code': 'HU', 'name': 'Hungary'}, {'code': 'ID', 'name': 'Indonesia'}, {'code': 'IE', 'name': 'Republic of Ireland'}, {'code': 'IL', 'name': 'Israel'}, {'code': 'IN', 'name': 'India'}, {'code': 'IQ', 'name': 'Iraq'}, {'code': 'IR', 'name': 'Iran'}, {'code': 'IS', 'name': 'Iceland'}, {'code': 'IT', 'name': 'Italy'}, {'code': 'JM', 'name': 'Jamaica'}, {'code': 'JO', 'name': 'Jordan'}, {'code': 'JP', 'name': 'Japan'}, {'code': 'KE', 'name': 'Kenya'}, {'code': 'KG', 'name': 'Kyrgyzstan'}, {'code': 'KI', 'name': 'Kiribati'}, {'code': 'KP', 'name': 'North Korea'}, {'code': 'KR', 'name': 'South Korea'}, {'code': 'KW', 'name': 'Kuwait'}, {'code': 'LB', 'name': 'Lebanon'}, {'code': 'LI', 'name': 'Liechtenstein'}, {'code': 'LR', 'name': 'Liberia'}, {'code': 'LS', 'name': 'Lesotho'}, {'code': 'LT', 'name': 'Lithuania'}, {'code': 'LU', 'name': 'Luxembourg'}, {'code': 'LV', 'name': 'Latvia'}, {'code': 'LY', 'name': 'Libya'}, {'code': 'MG', 'name': 'Madagascar'}, {'code': 'MH', 'name': 'Marshall Islands'}, {'code': 'MK', 'name': 'Macedonia'}, {'code': 'ML', 'name': 'Mali'}, {'code': 'MM', 'name': 'Myanmar'}, {'code': 'MN', 'name': 'Mongolia'}, {'code': 'MR', 'name': 'Mauritania'}, {'code': 'MT', 'name': 'Malta'}, {'code': 'MU', 'name': 'Mauritius'}, {'code': 'MV', 'name': 'Maldives'}, {'code': 'MW', 'name': 'Malawi'}, {'code': 'MX', 'name': 'Mexico'}, {'code': 'MY', 'name': 'Malaysia'}, {'code': 'MZ', 'name': 'Mozambique'}, {'code': 'NA', 'name': 'Namibia'}, {'code': 'NE', 'name': 'Niger'}, {'code': 'NG', 'name': 'Nigeria'}, {'code': 'NI', 'name': 'Nicaragua'}, {'code': 'NL', 'name': 'Kingdom of the Netherlands'}, {'code': 'NO', 'name': 'Norway'}, {'code': 'NP', 'name': 'Nepal'}, {'code': 'NR', 'name': 'Nauru'}, {'code': 'NZ', 'name': 'New Zealand'}, {'code': 'OM', 'name': 'Oman'}, {'code': 'PA', 'name': 'Panama'}, {'code': 'PE', 'name': 'Peru'}, {'code': 'PG', 'name': 'Papua New Guinea'}, {'code': 'PH', 'name': 'Philippines'}, {'code': 'PK', 'name': 'Pakistan'}, {'code': 'PL', 'name': 'Poland'}, {'code': 'PT', 'name': 'Portugal'}, {'code': 'PW', 'name': 'Palau'}, {'code': 'PY', 'name': 'Paraguay'}, {'code': 'QA', 'name': 'Qatar'}, {'code': 'RO', 'name': 'Romania'}, {'code': 'RU', 'name': 'Russia'}, {'code': 'RW', 'name': 'Rwanda'}, {'code': 'SA', 'name': 'Saudi Arabia'}, {'code': 'SB', 'name': 'Solomon Islands'}, {'code': 'SC', 'name': 'Seychelles'}, {'code': 'SD', 'name': 'Sudan'}, {'code': 'SE', 'name': 'Sweden'}, {'code': 'SG', 'name': 'Singapore'}, {'code': 'SI', 'name': 'Slovenia'}, {'code': 'SK', 'name': 'Slovakia'}, {'code': 'SL', 'name': 'Sierra Leone'}, {'code': 'SM', 'name': 'San Marino'}, {'code': 'SN', 'name': 'Senegal'}, {'code': 'SO', 'name': 'Somalia'}, {'code': 'SR', 'name': 'Suriname'}, {'code': 'ST', 'name': 'S\xc3\xa3o Tom\xc3\xa9 and Pr\xc3\xadncipe'}, {'code': 'SY', 'name': 'Syria'}, {'code': 'TG', 'name': 'Togo'}, {'code': 'TH', 'name': 'Thailand'}, {'code': 'TJ', 'name': 'Tajikistan'}, {'code': 'TM', 'name': 'Turkmenistan'}, {'code': 'TN', 'name': 'Tunisia'}, {'code': 'TO', 'name': 'Tonga'}, {'code': 'TR', 'name': 'Turkey'}, {'code': 'TT', 'name': 'Trinidad and Tobago'}, {'code': 'TV', 'name': 'Tuvalu'}, {'code': 'TZ', 'name': 'Tanzania'}, {'code': 'UA', 'name': 'Ukraine'}, {'code': 'UG', 'name': 'Uganda'}, {'code': 'US', 'name': 'United States'}, {'code': 'UY', 'name': 'Uruguay'}, {'code': 'UZ', 'name': 'Uzbekistan'}, {'code': 'VA', 'name': 'Vatican City'}, {'code': 'VE', 'name': 'Venezuela'}, {'code': 'VN', 'name': 'Vietnam'}, {'code': 'VU', 'name': 'Vanuatu'}, {'code': 'YE', 'name': 'Yemen'}, {'code': 'ZM', 'name': 'Zambia'}, {'code': 'ZW', 'name': 'Zimbabwe'}, {'code': 'DZ', 'name': 'Algeria'}, {'code': 'BA', 'name': 'Bosnia and Herzegovina'}, {'code': 'KH', 'name': 'Cambodia'}, {'code': 'CF', 'name': 'Central African Republic'}, {'code': 'TD', 'name': 'Chad'}, {'code': 'KM', 'name': 'Comoros'}, {'code': 'HR', 'name': 'Croatia'}, {'code': 'TL', 'name': 'East Timor'}, {'code': 'SV', 'name': 'El Salvador'}, {'code': 'GQ', 'name': 'Equatorial Guinea'}, {'code': 'GD', 'name': 'Grenada'}, {'code': 'KZ', 'name': 'Kazakhstan'}, {'code': 'LA', 'name': 'Laos'}, {'code': 'FM', 'name': 'Federated States of Micronesia'}, {'code': 'MD', 'name': 'Moldova'}, {'code': 'MC', 'name': 'Monaco'}, {'code': 'ME', 'name': 'Montenegro'}, {'code': 'MA', 'name': 'Morocco'}, {'code': 'KN', 'name': 'Saint Kitts and Nevis'}, {'code': 'LC', 'name': 'Saint Lucia'}, {'code': 'VC', 'name': 'Saint Vincent and the Grenadines'}, {'code': 'WS', 'name': 'Samoa'}, {'code': 'RS', 'name': 'Serbia'}, {'code': 'ZA', 'name': 'South Africa'}, {'code': 'ES', 'name': 'Spain'}, {'code': 'LK', 'name': 'Sri Lanka'}, {'code': 'SZ', 'name': 'Swaziland'}, {'code': 'CH', 'name': 'Switzerland'}, {'code': 'AE', 'name': 'United Arab Emirates'}, {'code': 'GB', 'name': 'United Kingdom'}]

        return Response(all_countries)


class ForgotPassword(APIView):

    # create a new user
    def post(self, request, *args, **kwargs):

        user_email = request.data['email']
        if User.objects.filter(email=user_email).exists():
            email = User.objects.get(email=request.POST['email'])
            user = UserProfiles.objects.get(user=email)
            site = Site.objects.get(pk=1)
            t = loader.get_template('password.txt')
            c = Context({'name': email.first_name, 'email': email, 'site': site.name, 'token': user.token})
            send_mail('[%s] %s' % (site.name, 'New Contactus Request'), t.render(c), 'scorpionspython@gmail.com',
                      [email.email], fail_silently=False)
            return Response({'code': 1, 'status': 200, 'Data': 'Null', 'message': 'Email has been sent'})

        else:
            return Response({'code': 0, 'status': 200, 'message': 'User does not exist'})