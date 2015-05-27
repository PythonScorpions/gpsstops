from django.conf.urls import patterns, include, url
from api.views import *

urlpatterns = patterns("api.views",
                       url(r'create_user', CreateUser.as_view(), name='create-user'),
                       url(r'update_user/(?P<pk>[a-zA-Z0-9]+)', UpdateUser.as_view(), name='update-user'),
                       url(r'login', LoginUser.as_view(), name='login-user'),
                       url(r'current_user_details/(?P<pk>[a-zA-Z0-9]+)', CurrentUser.as_view(), name='current-user'),
                       )