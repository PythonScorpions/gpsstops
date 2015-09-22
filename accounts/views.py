'''
'''
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.models import Site
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect, render
from django.template import loader, RequestContext, Context
from django.views.generic import TemplateView, UpdateView, View
from django.utils.decorators import method_decorator
from django.conf import settings
from django.db.models import Q

from accounts.forms import *
from maps.models import *
from maps.views import custom_login_required

from os import urandom
import datetime, random, string


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
                url_to_direct = '/maps/routes/'
            else:
                url_to_direct = '/route/add/'

        return render(request, self.template_name, locals())


def register(request):
    template_name = 'signup2.html'
    form = RegisterForm()
    if request.method == 'POST':
        print "yo"
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Organization Entry
            user_obj = User.objects.get(id=user.user.id)
            Organization(super_admin=user_obj).save()

            request.session['token'] = user.token
            message = '%s/verification/%s/' % (settings.SERVER_URL, user.token)
            print user.user.email

            t = loader.get_template('verification.txt')
            c = Context({'varification_link': message})
            send_mail('Welcome to gpsstops.com', t.render(c),
                settings.EMAIL_HOST_USER, [str(user.user.email)],
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
            print email, password
            user = authenticate(username=email, password=password)

            if user is not None:
                admin_status = UserProfiles.objects.get(user__email=str(email)).admin_status
                if admin_status == 'disabled':
                    print "in disable mode"
                    messages.success(request, "Your account has been disabled by Admin..")
                    return render_to_response(self.template_name, locals(), context_instance=RequestContext(request))
                if user.is_active:
                    print "going here"
                    login(request, user)
                    return redirect('/calender/')
                else:
                    messages.success(request, "Your account is not activated yet, please check your email")
            else:
                messages.success(request, "Invalid Email or Password")

        return render_to_response(self.template_name, locals(), context_instance=RequestContext(request))


def user_logout(request):
    logout(request)
    return redirect('/')


class Calender(TemplateView):
    template_name = 'calendar_phase.html'

    @method_decorator(custom_login_required)
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
                url_to_direct = '/maps/routes/'
            else:
                url_to_direct = '/route/add/'

        return render(request, self.template_name, locals())


class ForgotPassword(TemplateView):

    template_name = 'forgotpassword.html'

    def post(self, request, *args, **kwargs):
        if User.objects.filter(email=request.POST['email']).exists():
            email = User.objects.get(email=request.POST['email'])
            user = UserProfiles.objects.get(user=email)

            site = settings.SERVER_URL
            t = loader.get_template('password.txt')
            c = Context({
                    'name': email.first_name,
                    'email': email,
                    'site': site,
                    'token': user.token
                })

            send_mail(
                '[%s] %s' % (site, 'New Contactus Request'),
                t.render(c),
                settings.EMAIL_HOST_USER,
                [email.email],
                fail_silently=False
            )
            messages.success(request, 'Password reset link has been sent to your email')

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

    @method_decorator(custom_login_required)
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

    @method_decorator(custom_login_required)
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

    @method_decorator(custom_login_required)
    def get(self, request):

        if request.user.is_authenticated():
            today = datetime.date.today()
            today_routes = Route.objects.filter(user=request.user)
            final_routes = False
            for route in today_routes:
                if route.trip_datetime.day == today.day and \
                    route.trip_datetime.year == today.year and \
                    route.trip_datetime.month == today.month:
                        final_routes = True
                        break

            if final_routes:
                url_to_direct = '/maps/routes/'
            else:
                url_to_direct = '/route/add/'
                form = RouteAssignmentForm(user=request.user)

        active = "maps"
        flag="maps"
        return render(request, self.template1, locals())


class Download(TemplateView):
    template_name = 'download.html'


class Support(TemplateView):
    template_name = 'support.html'


class Contact(TemplateView):
    template_name = 'contact.html'


class About(TemplateView):
    template_name = 'about.html'


class LearnMore(TemplateView):
    template_name = 'learn_more.html'


def get_users_list(user):
    if user.user_profiles.user_role == "super_admin":
        users = User.objects \
                .filter(
                    Q(user_profiles__admin=user) |
                    Q(user_profiles__admin__user_profiles__admin=user)
                )
    else:
        users = User.objects \
                .filter(
                    Q(user_profiles__admin=user) |
                    Q(user_profiles__admin=user.user_profiles.admin)
                ) \
                .filter(user_profiles__user_role="employee")

    return users

class UsersView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.user_profiles.user_role in ['super_admin', 'admin']:
            return redirect('/')

        users = get_users_list(request.user)

        return render(request, 'accounts/accounts_list.html', {'users':users})
users_view = UsersView.as_view()


class UsersCreateView(View):

    def _generate_token(self):
        alphabet = [c for c in string.letters + string.digits if ord(c) < 128]
        return ''.join([random.choice(alphabet) for x in xrange(30)])

    def _generate_password(self, length):
        if not isinstance(length, int) or length < 8:
            raise ValueError("temp password must have positive length")

        chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
        return "".join([chars[ord(c) % len(chars)] for c in urandom(length)])

    def _get_form_class(self, user):
        print user.user_profiles.user_role
        if user.user_profiles.user_role == "super_admin":
            form_class = UsersCreateSuperAdminForm
        else:
            form_class = UsersCreateForm
        return form_class

    def get(self, request, pk=None, *args, **kwargs):
        if request.user.is_authenticated() and \
            (not request.user.user_profiles.user_role in ['super_admin', 'admin']):
                return redirect('/')

        user = None
        if pk:
            try:
                users = get_users_list(request.user)
                user = users.get(id=pk)
            except:
                redirect('/accounts/users/')

        form_class = self._get_form_class(request.user)

        if user:
            initial_data = {
                'email':user.email,
                'first_name':user.first_name,
                'last_name':user.last_name,
                'is_active':user.is_active
            }
            # print initial_data
            form = form_class(user=request.user,
                        instance=user.user_profiles, initial=initial_data)
        else:
            form = form_class(user=request.user)

        template_data = {'form':form}
        return render(request, 'accounts/users_create.html', template_data)

    def post(self, request, pk=None, *args, **kwargs):
        if request.user.is_authenticated() and \
            (not request.user.user_profiles.user_role in ['super_admin', 'admin']):
                return redirect('/')

        if request.user.user_profiles.user_role == 'admin':
            print "yes it is admin who is logged in"
            org_obj = Organization.objects.get(super_admin=request.user.user_profiles.admin)
        else:
            print "yes it is super admin who is logged in"
            org_obj = Organization.objects.get(super_admin__id=request.user.id)

        user = None
        if pk:
            try:
                users = get_users_list(request.user)
                user = users.get(id=pk)
            except:
                redirect('/accounts/users/')

        form_class = self._get_form_class(request.user)

        if user:
            user_current_role = user.user_profiles.user_role
            form = form_class(data=request.POST,
                        user=request.user, instance=user.user_profiles)
        else:
            form = form_class(data=request.POST, user=request.user)

        if form.is_valid():

            if not user:
                # generate password
                new_password = self._generate_password(10)

            # save user with password
            if user:
                form.instance.user.first_name = form.cleaned_data['first_name']
                form.instance.user.last_name = form.cleaned_data['last_name']
                # form.instance.user.is_active = form.cleaned_data.get('is_active', False)
                form.instance.user.save()
                user_new_role = user.user_profiles.user_role
                if user_current_role != user_new_role:
                    if user_current_role == 'admin':
                        org_obj.admins.remove(user)
                        org_obj.employees.add(user)
                    else:
                        org_obj.employees.remove(user)
                        org_obj.admins.add(user)

            else:
                new_user = User(email=form.cleaned_data['email'], username=form.cleaned_data['email'])
                new_user.first_name = form.cleaned_data['first_name']
                new_user.last_name = form.cleaned_data['last_name']
                new_user.password = make_password(new_password)
                new_user.is_active = True
                new_user.save()

                # save user profile
                new_token = self._generate_token()
                form.instance.user = new_user
                form.instance.admin_status = 'enable'
                form.instance.token = new_token
                form.instance.admin = request.user
                form.instance.company_name = " "
                form.instance.occupation = " "

            user_profile = form.save()
            print "------------------------------------------------", user_profile.user_role

            if not user:
                if user_profile.user_role == 'admin':
                    org_obj.admins.add(new_user)
                else:
                    org_obj.employees.add(new_user)

            if not user:
                # send password email with token
                url = '%s/accounts/login/%s/' % (settings.SERVER_URL, user_profile.token)
                message = 'Please login using this link %s with password %s' % (url, new_password)

                send_mail('Login Link', message, settings.EMAIL_HOST_USER,
                    [str(new_user.email)], fail_silently=False)

            return redirect('/accounts/users/')
        else:
            print form.errors

        template_data = {'form':form}
        return render(request, 'accounts/users_create.html', template_data)
users_create_view = UsersCreateView.as_view()


class UsersLogin(View):
    def get(self, request, *args, **kwargs):
        try:
            user_profile = UserProfiles.objects.get(token=str(kwargs['key']))
        except:
            print "No token found"
        else:
            form = UsersLoginForm()

            return render(request, 'accounts/login.html', {'form':form})
        return redirect('/')

    def post(self, request, *args, **kwargs):
        try:
            user_profile = UserProfiles.objects.get(token=str(kwargs['key']))
        except:
            print "No token found"
        else:
            form = UsersLoginForm(request.POST)

            if form.is_valid():
                user_profile.user.set_password(form.cleaned_data['password'])
                user_profile.user.is_active = True
                user_profile.user.save()
                return redirect('/')
            else:
                print form.errors
            return render(request, 'accounts/login.html', {'form':form})
        return redirect('/')
users_login_view = UsersLogin.as_view()


class UserActivatedView(View):
    def get(self, request, pk=None, *args, **kwargs):
        user = None
        if pk:
            try:
                users = get_users_list(request.user)
                user = users.get(id=pk)
            except:
                pass
            else:
                user.is_active = not user.is_active
                user.save()

        return redirect('/accounts/users/')
users_enable_view = UserActivatedView.as_view()


class ThemeView(View):

    @method_decorator(login_required)
    def get(self, request, pk=None, *args, **kwargs):
        if not request.user.user_profiles.user_role == "super_admin":
            return redirect("/")

        context = {}
        try:
            organization = Organization.objects.get(super_admin=request.user)
        except:
            context['error_message'] = "Error! User is not assigned an organization. Please contact your administrator."

        if not organization.theme:
            organization.theme = Theme.objects.create()
            organization.save()

        if not organization.web_theme:
            organization.web_theme = WebTheme.objects.create()
            organization.save()

        context['web_theme_form'] = WebThemeForm(instance=organization.web_theme)
        context['mobile_theme_form'] = MobileThemeForm(instance=organization.theme)

        return render(request, "accounts/theme.html", context)

    @method_decorator(login_required)
    def post(self, request, pk=None, *args, **kwargs):
        if not request.user.user_profiles.user_role == "super_admin":
            return redirect("/")

        context = {}
        try:
            organization = Organization.objects.get(super_admin=request.user)
        except:
            context['error_message'] = "Error! User is not assigned an organization. Please contact your administrator."

        if not organization.theme:
            organization.theme = Theme.objects.create()
            organization.save()

        if not organization.web_theme:
            organization.web_theme = WebTheme.objects.create()
            organization.save()

        if request.POST.has_key('web_theme'):
            web_theme_form = WebThemeForm(request.POST, request.FILES, instance=organization.web_theme)
            context['web_theme_form'] = web_theme_form

            if web_theme_form.is_valid():
                web_theme_form.save()
            else:
                print web_theme_form.errors
        else:
            context['web_theme_form'] = WebThemeForm(instance=organization.web_theme)

        if request.POST.has_key('mobile_theme'):
            mobile_theme_form = MobileThemeForm(request.POST, request.FILES, instance=organization.theme)
            context['mobile_theme_form'] =  mobile_theme_form

            if mobile_theme_form.is_valid():
                mobile_theme_form.save()
            else:
                print mobile_theme_form.errors
        else:
            context['mobile_theme_form'] = MobileThemeForm(instance=organization.theme)

        return render(request, "accounts/theme.html", context)
theme_view = ThemeView.as_view()


class CssThemeView(View):
    def get(self, request, pk=None, *args, **kwargs):
        organization = None
        try:
            if request.user.user_profiles.user_role == "super_admin":
                organization = Organization.objects.get(super_admin=request.user)
            elif request.user.user_profiles.user_role == "admin":
                organization = Organization.objects.get(admins=request.user)
            elif request.user.user_profiles.user_role == "employee":
                organization = Organization.objects.get(employees=request.user)
        except:
            pass

        if organization == None:
            return render(request, '')
        # print organization.web_theme.logo
        return render(request, 'accounts/theme.css',
            {'theme':organization.web_theme}, content_type='text/css')
css_theme_view = CssThemeView.as_view()
