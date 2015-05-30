from django.conf.urls import patterns, include, url
from maps.views import *

urlpatterns = patterns("maps.views",
                       url(r'create_route$', Create_Route.as_view(), name='create_route'),
                       url(r'edit_route/(?P<id>.*)/$', Edit_Route.as_view(), name='edit_route'),
                    #    url(r'signup$', register, name='signup'),
                       )
