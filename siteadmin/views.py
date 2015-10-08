'''
'''
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView, UpdateView, View
from django.shortcuts import render_to_response, redirect, render
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator

from accounts.models import *
from siteadmin.forms import *
from siteadmin.models import *


def admin_login_required(f):
   def wrap(request, *args, **kwargs):
       # this will check whether admin user is logged in , if not it will redirect to login page
       if request.user.is_authenticated() and request.user.is_superuser:
           pass
       else:
           return render(request, "siteadmin/login.html", locals())
       return f(request, *args, **kwargs)

   wrap.__doc__ = f.__doc__
   wrap.__name__ = f.__name__
   return wrap


class IndexView(View):
    template_name = 'siteadmin/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_active and request.user.is_authenticated and request.user.is_superuser is True:
            user_details = User.objects.filter(is_staff=False).order_by('id')
            return render(request, "siteadmin/users.html", locals())
        return render(request, self.template_name, locals())

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)
        if user and user.is_active and user.is_superuser:
                login(request, user)
                user_details = User.objects.filter(is_staff=False).order_by('id')
                return render(request, 'siteadmin/users.html', locals())
        else:
            error_message = "Username and Password does not match"
            return render(request, 'siteadmin/login.html', locals())

        # if form.is_valid():
        #     user = authenticate(username=username, password=password)
        #     print user,
        #     if user and user.is_active and user.is_superuser:
        #         login(request, user)
        #         print "User is valid, active and authenticated"
        #         user_data = user_profile.objects.all().order_by('id')
        #         return render(request, 'siteadmin/index.html', locals())
        #     else:
        #         error = "Invalid username or Password!"
        #         print "The password is valid, but the account has been disabled!"
        #         return render(request, 'siteadmin/login.html', locals())
        # else:
        #     print form.errors
        #     return render(request, 'siteadmin/login.html', locals())


def admin_logout(request):
    print "jhfdkjhj"
    logout(request)
    print "jnkjsd"
    return redirect('/admin')


class UserDetails(View):
    template_name = 'siteadmin/user-details.html'

    @method_decorator(admin_login_required)
    def get(self, request, *args, **kwargs):
        user_id = self.kwargs['id']
        user_details = User.objects.get(id=int(user_id))
        print user_details
        return render(request, self.template_name, locals())


class DeleteUser(View):

    @method_decorator(admin_login_required)
    def get(self, request, user_id):
        User.objects.get(id=int(user_id)).delete()
        return HttpResponse('success')


class EnableUser(View):

    @method_decorator(admin_login_required)
    def get(self, request, user_id):
        print "jhj-----------------------------------------------"
        profile_data = UserProfiles.objects.get(user__id=int(user_id))
        profile_data.admin_status = 'enable'
        profile_data.save()
        return HttpResponseRedirect('success')


class DisableUser(View):

    @method_decorator(admin_login_required)
    def get(self, request, user_id):
        profile_data = UserProfiles.objects.get(user__id=int(user_id))
        profile_data.admin_status = 'disabled'
        profile_data.save()
        return HttpResponse('success')


class HelpSectionView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_active and request.user.is_authenticated and \
            request.user.is_superuser is True:
            context_data = {
                'help_sections': HelpSection.objects.all()
            }
            return render(request, "siteadmin/help_section.html", context_data)
        return redirect("/admin/")
help_section_view = HelpSectionView.as_view()


class HelpSectionEditView(View):
    def get(self, request, pk=None, *args, **kwargs):
        if request.user.is_active and request.user.is_authenticated and \
            request.user.is_superuser is True:
            if pk:
                try:
                    help_section = HelpSection.objects.get(pk=pk)
                except:
                    help_section = None

            if help_section:
                form = HelpSectionForm(instance=help_section)
            else:
                form = HelpSectionForm()
            context_data = {'form':form}
            return render(request, "siteadmin/help_section_edit.html", context_data)
        return redirect("/admin/")

    def post(self, request, pk=None, *args, **kwargs):
        if request.user.is_active and request.user.is_authenticated and \
            request.user.is_superuser is True:
            if pk:
                try:
                    help_section = HelpSection.objects.get(pk=pk)
                except:
                    help_section = None

            if help_section:
                form = HelpSectionForm(request.POST, instance=help_section)
            else:
                form = HelpSectionForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('/admin/help_section/')
            else:
                print form.errors
            context_data = {'form':form}
            return render(request, "siteadmin/help_section_edit.html", context_data)
        return redirect("/admin/")
edit_help_section_view = HelpSectionEditView.as_view()