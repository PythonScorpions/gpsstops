from django.conf.urls import patterns, include, url
from siteadmin.views import *

urlpatterns = patterns("siteadmin.views",
                       url(r'^$', IndexView.as_view(), name='admin-index'),
                       url(r'admin_logout', user_logout, name='admin-logout'),
                       url(r'view_user_details/(?P<id>\w+)/$', UserDetails.as_view(), name='user-details'),
                       url('^delete_user/(?P<user_id>[a-zA-Z0-9]+)$', DeleteUser.as_view(),
                           name="delete-user"),
                       url('^enable_user/(?P<user_id>[a-zA-Z0-9]+)$', EnableUser.as_view(),
                           name="delete-user"),
                       url('^disable_user/(?P<user_id>[a-zA-Z0-9]+)$', DisableUser.as_view(),
                           name="delete-user"),
                       )