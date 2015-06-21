from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
                       url(r'^', include('accounts.urls')),
                       url(r'^maps/', include('maps.urls')),
                       url(r'^api/', include('api.urls')),
                       url(r'^admin/', include('siteadmin.urls')),
                       )
