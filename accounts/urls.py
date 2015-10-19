'''
'''
from django.conf.urls import patterns, include, url
from accounts.views import *

urlpatterns = patterns("accounts.views",
    url(r'^$', IndexView.as_view(), name='index'),

    # url(r'signup$', register, name='signup'),
    url(r'signup$', signup_view, name='signup'),

    url(r'email-sent/$', EmailSent.as_view(), name='email-sent'),
    url(r'verification/(?P<key>\w+)/$', Verification.as_view(), name='verification'),
    url(r'^login/$', LoginView.as_view(), name='login-view'),
    url(r'calender/$', Calender.as_view(), name='calender_prime'),
    url(r'route/add/$', Add_route_prime.as_view(), name='add_route_prime'),
    url(r'forgot-password/$', ForgotPassword.as_view(), name='forgot-password'),
    url(r'^reset-password/(?P<key>\w+)/$', ResetPassword.as_view(), name='reset-password'),
    url(r'^customer-reset-password/(?P<key>\w+)/$', CustomerResetPassword.as_view(), name='customer-reset-password'),
    url(r'^logout/$', user_logout, name='user_logout'),
    url(r'^update-profile/$', UpdateProfile.as_view(), name='update-profile'),
    # url(r'account-confirmed', AccountConfirmed.as_view(), name='account-confirmed'),
    # url(r'^accounts/', include('registration.backends.default.urls')),
    # url(r'posts/add-post/$', 'addpost', name='add-post')

    # users management
    url(r'^accounts/users/$', users_view, name='users_list'),
    url(r'^accounts/users/create/$', users_create_view, name='users_create'),
    url(r'^accounts/users/(?P<pk>\d+)/$', users_create_view, name='users_edit'),
    url(r'^accounts/users/(?P<pk>\d+)/active/toggle/$', users_enable_view, name='users_enable'),
    url(r'^accounts/login/(?P<key>\w+)/$', users_login_view, name='users_login'),

    url(r'^accounts/theme/$', theme_view, name='theme'),
    url(r'^accounts/theme/css/$', css_theme_view, name='css-theme'),


    url(r'^payment/paypal/$', payment_processing_view, name='payment_processing_view'),

    url(r'accounts/company_registration/$', CompanyRegi.as_view(), name='company-registration'),
    url(r'accounts/customer_followers/$', CustomerFollowers.as_view(), name='customer-followers'),

    url(r'^help/$', help_view, name='help_view'),
)