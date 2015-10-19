from django.conf.urls import patterns, include, url
from siteadmin.views import *
from siteadmin import views

urlpatterns = patterns("siteadmin.views",
    url(r'^$', IndexView.as_view(), name='admin-index'),
    url(r'admin_logout$', views.admin_logout, name='admin-logout'),

    url(r'view_user_details/(?P<id>\w+)/$', UserDetails.as_view(), name='user-details'),
    url('^delete_user/(?P<user_id>[a-zA-Z0-9]+)/$', DeleteUser.as_view(), name="delete-user"),
    url('^enable_user/(?P<user_id>[a-zA-Z0-9]+)/$', EnableUser.as_view(), name="delete-user"),
    url('^disable_user/(?P<user_id>[a-zA-Z0-9]+)/$', DisableUser.as_view(), name="delete-user"),

    url('^help_section/$', help_section_view, name="admin_help_section"),
    url('^help_section/add/$', edit_help_section_view, name="admin_help_section_edit"),
    url('^help_section/(?P<pk>\d+)/edit/$', edit_help_section_view, name="admin_help_section_edit"),

    url('^subscription/users/$', subscription_users_view, name="subscription-users"),
)