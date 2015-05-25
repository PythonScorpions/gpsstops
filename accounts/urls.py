from django.conf.urls import patterns, include, url
from accounts.views import *

urlpatterns = patterns("accounts.views",
                       url(r'^$', IndexView.as_view(), name='index'),
                       url(r'signup$', register, name='signup'),
                       url(r'email-sent', EmailSent.as_view(), name='email-sent'),
                       url(r'verification/(?P<key>\w+)/$', Verification.as_view(), name='verification'),
                       url(r'login', LoginView.as_view(), name='login-view'),
                       url(r'calender', Calender.as_view(), name='calender'),
                       # url(r'account-confirmed', AccountConfirmed.as_view(), name='account-confirmed'),
                       # url(r'^accounts/', include('registration.backends.default.urls')),
                       # url(r'posts/add-post/$', 'addpost', name='add-post')
                       )