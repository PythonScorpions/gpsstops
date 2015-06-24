from django.conf.urls import patterns, include, url
from accounts.views import *

urlpatterns = patterns('',
                       url(r'^', include('accounts.urls')),
                       url(r'^maps/', include('maps.urls')),
                       url(r'^api/', include('api.urls')),
                       url(r'^admin/', include('siteadmin.urls')),
                       url(r'download/', Download.as_view(), name='download'),
                       url(r'support/', Support.as_view(), name='support'),
                       url(r'contact_us/', Contact.as_view(), name='contact'),
                       url(r'about_us/', About.as_view(), name='about'),
                       url(r'learn_more', LearnMore.as_view(), name='learn-more'),
                       )
