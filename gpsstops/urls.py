from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
                       url(r'^', include('accounts.urls')),
                       url(r'^maps/', include('maps.urls')),
                       url(r'^api/', include('api.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       )
