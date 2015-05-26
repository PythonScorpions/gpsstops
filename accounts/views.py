__author__ = 'Scorpion_Python'
from django.views.generic.base import TemplateView
from django.shortcuts import render_to_response, redirect, render
from accounts.forms import *
from django.views.generic import View
from django.template import RequestContext, Context
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


class IndexView(TemplateView):
    template_name = 'index.html'

    def dispatch(self, *args, **kwargs):
        return super(IndexView, self).dispatch(*args, **kwargs)


def register(request):
    template_name = 'signup2.html'
    form = RegisterForm()
    if request.method == 'POST':
        print "yo"
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            request.session['token'] = user.token
            message = 'Please verify your email by clicking on this link ' + 'http://localhost:8000/verfification/'+user.token
            print user.user.email
            send_mail('Verification Link', message, 'testing.zealousys@gmail.com', [str(user.user.email)],
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
        return render_to_response(self.template_name, context_instance=RequestContext(request),)


class Calender(TemplateView):

    template_name = 'calendar_prime.html'


class Add_route_prime(View):
    template1 = "add-route.html"
    template2 = "add-route.html"

    def get(self, request):
        active = "maps"
        flag="maps"
        return render(request, self.template1, locals())

    def post(self, request):
        active = "maps"
        flag="maps"
        return render(request, self.template2, locals())
