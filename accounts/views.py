from django.views.generic import TemplateView, UpdateView, View
from django.shortcuts import render_to_response, redirect, render
from accounts.forms import *
from django.template import RequestContext, Context
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.template import loader
from django.contrib.sites.models import Site
from maps.models import *
import datetime
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class IndexView(View):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):

        if request.user.is_authenticated():
            today = datetime.date.today()
            today_routes = Route.objects.filter(user=request.user)
            final_routes = False
            for route in today_routes:
                if route.trip_datetime.day == today.day and route.trip_datetime.year == today.year and route.trip_datetime.month == today.month:
                    final_routes = True
                    break

            if final_routes:
                url_to_direct = '/maps/routes'
            else:
                url_to_direct = '/route/add'

        return render(request, self.template_name, locals())


def register(request):
    template_name = 'signup2.html'
    form = RegisterForm()
    if request.method == 'POST':
        print "yo"
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            request.session['token'] = user.token
            message = 'Please verify your email by clicking on this link ' + 'http://gpsstops.pythonanywhere.com/verification/'+user.token
            print user.user.email
            send_mail('Verification Link', message, 'scorpionspython@gmail.com', [str(user.user.email)],
                      fail_silently=False)
            print "yes sent"
            return redirect('email-sent')
        else:
            print "errors", form.errors
    return render_to_response(template_name, {'form': form}, context_instance=RequestContext(request),)


class EmailSent(TemplateView):
    template_name = 'email_sent.html'


class Verification(TemplateView):
    template_name = 'confirmed_email.html'

    def get(self, request, *args, **kwargs):
        if UserProfiles.objects.filter(token=str(kwargs['key'])).exists():

            user = UserProfiles.objects.get(token=kwargs['key'])
            user.user.is_active = True
            user.user.save()
        return render_to_response(self.template_name, context_instance=RequestContext(request),)


class LoginView(TemplateView):

    template_name = 'index.html'

    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            # message = ''
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(username=email, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/calender')
                else:
                    messages.success(request, "Your account is not activated yet, please check your email")
            else:
                messages.success(request, "Invalid Email or Password")

        return render_to_response(self.template_name, locals(), context_instance=RequestContext(request))


def user_logout(request):
    logout(request)
    return redirect('/')


class Calender(TemplateView):
    template_name = 'calendar_prime.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):

        if request.user.is_authenticated():
            today = datetime.date.today()
            today_routes = Route.objects.filter(user=request.user)
            final_routes = False
            for route in today_routes:
                if route.trip_datetime.day == today.day and route.trip_datetime.year == today.year and route.trip_datetime.month == today.month:
                    final_routes = True
                    break

            if final_routes:
                url_to_direct = '/maps/routes'
            else:
                url_to_direct = '/route/add'

        return render(request, self.template_name, locals())


class ForgotPassword(TemplateView):

    template_name = 'forgotpassword.html'

    def post(self, request, *args, **kwargs):
        if User.objects.filter(email=request.POST['email']).exists():
            email = User.objects.get(email=request.POST['email'])
            user = UserProfiles.objects.get(user=email)
            site = Site.objects.get(pk=1)
            t = loader.get_template('password.txt')
            c = Context({'name': email.first_name, 'email': email, 'site': site.name, 'token': user.token})
            send_mail('[%s] %s' % (site.name, 'New Contactus Request'), t.render(c), 'scorpionspython@gmail.com',
                      [email.email], fail_silently=False)
            messages.success(request, 'Reset link has sent to your email')

        else:
            messages.success(request, 'User with this email Doesnt exist')
        return render_to_response(self.template_name, context_instance=RequestContext(request),)


class ResetPassword(TemplateView):

    template_name = 'change-password.html'
    template2_name = 'index.html'

    def post(self, request, *args, **kwargs):
        print "yes"
        user = UserProfiles.objects.get(token=kwargs['key'])
        if user and request.POST['password1'] == request.POST['password2']:
            user_data = User.objects.get(id=int(user.user.id))
            user_data.password = make_password(request.POST['password2'])
            user_data.save()
            print "yes 2"
            return render_to_response(self.template2_name, context_instance=RequestContext(request),)
        else:
            messages.success(request, 'Please Make Sure Two password Fields are Same')
        return render_to_response(self.template_name, context_instance=RequestContext(request),)


class UpdateProfile(UpdateView):
    template_name = 'my-account.html'
    form_class = ProfileUpdateForm

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        user = User.objects.get(username=request.user)
        profile = UserProfiles.objects.get(user=user)
        id = user.id
        form = self.form_class({'first_name': profile.user.first_name, 'email': profile.user.email,
                                'country': profile.country, 'state': profile.state, 'city': profile.state,
                                'phone_number': profile.phone_number, 'occupation': profile.occupation,
                                'company_name': profile.company_name, 'address': profile.address,
                                'zip_code': profile.zip_code})
        return render_to_response(self.template_name, {'form': form, 'id': id},
                                  context_instance=RequestContext(request),)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        user = User.objects.get(username=request.user)
        profile = UserProfiles.objects.get(user=user)
        form = self.form_class(request.POST, instance=user)
        if form.is_valid():
            profile.phone_number = request.POST['phone_number']
            profile.company_name = request.POST['company_name']
            profile.zip_code = request.POST['zip_code']
            profile.address = request.POST['address']
            profile.state = request.POST['state']
            profile.city = request.POST['city']
            profile.occupation = request.POST['occupation']
            profile.country = request.POST['country']
            user.first_name = request.POST['first_name']
            user.email = request.POST['email']
            user.save()
            profile.save()
            messages.success(request, 'Profile Editted Successfully.')
            return redirect('/update-profile')
        return render_to_response(self.template_name, {'form': form, 'id': id},
                                  context_instance=RequestContext(request))


class Add_route_prime(View):
    template1 = "add-route.html"
    template2 = "add-route.html"

    @method_decorator(login_required)
    def get(self, request):

        if request.user.is_authenticated():
            today = datetime.date.today()
            today_routes = Route.objects.filter(user=request.user)
            final_routes = False
            for route in today_routes:
                if route.trip_datetime.day == today.day and route.trip_datetime.year == today.year and route.trip_datetime.month == today.month:
                    final_routes = True
                    break

            if final_routes:
                url_to_direct = '/maps/routes'
            else:
                url_to_direct = '/route/add'

        active = "maps"
        flag="maps"
        return render(request, self.template1, locals())
