'''
'''
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from accounts.views import *


urlpatterns = patterns('',

   url(r'^', include('accounts.urls')),
   url(r'^maps/', include('maps.urls')),
   url(r'^api/', include('api.urls')),
   url(r'^appointments/', include('appointments.urls')),
   url(r'^custom_forms/', include('custom_forms.urls')),
   url(r'^products/', include('products.urls')),
   url(r'^services/', include('services.urls')),
   url(r'^admin/', include('siteadmin.urls')),
   url(r'download/$', Download.as_view(), name='download'),
   url(r'support/$', Support.as_view(), name='support'),
   url(r'contact_us/$', Contact.as_view(), name='contact'),
   url(r'about_us/$', About.as_view(), name='about'),
   url(r'learn_more/$', LearnMore.as_view(), name='learn-more'),
   url(r'faqs/$', FAQsView.as_view(), name='faqs'),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
