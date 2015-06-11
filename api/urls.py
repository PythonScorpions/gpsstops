from django.conf.urls import patterns, include, url
from api.views import *
from rest_framework.authtoken import views

urlpatterns = patterns("api.views",
                       url(r'create_user', CreateUser.as_view(), name='create-user'),
                       url(r'update_user/(?P<pk>[a-zA-Z0-9]+)', UpdateUser.as_view(), name='update-user'),
                       url(r'^api-token-auth/', ObtainAuthToken.as_view(), name='token-check'),
                       url(r'current_user_details/(?P<pk>[a-zA-Z0-9]+)', CurrentUser.as_view(), name='current-user'),
                       url(r'country_list', CountryList.as_view(), name='country-list'),
                       url(r'forgot_password', ForgotPassword.as_view(), name='country-list'),
                       url(r'create_route', CreateRouteApi.as_view(), name='create-route-api'),
                       url(r'route_list/(?P<pk>[a-zA-Z0-9]+)', RouteListApi.as_view(), name='route-list-api'),
                       url(r'edit_route/(?P<pk>[a-zA-Z0-9]+)', EditRouteApi.as_view(), name='edit-route-api'),
                       url(r'events', Events.as_view(), name='events-api'),
                       )