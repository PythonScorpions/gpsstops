from django.conf.urls import patterns, include, url
from api.views import *

from rest_framework import routers
from rest_framework.authtoken import views


# Routers provide an easy way of automatically determining the URL conf.
router = routers.SimpleRouter()
router.register(r'appointments', AppointmentsViewSet, base_name='Appointments')
router.register(r'task', TaskViewSet, base_name='Task')
router.register(r'contact', ContactViewSet, base_name='Contact')
router.register(r'contact_group', ContactGroupViewSet, base_name='ContactGroup')


urlpatterns = patterns("api.views",
    url(r'create_user', CreateUser.as_view(), name='create-user'),
    url(r'update_user/(?P<pk>[a-zA-Z0-9]+)', UpdateUser.as_view(), name='update-user'),
    url(r'^api-token-auth/', ObtainAuthToken.as_view(), name='token-check'),
    url(r'^logout/', LogoutUser.as_view(), name='logout'),
    url(r'current_user_details/(?P<pk>[a-zA-Z0-9]+)', CurrentUser.as_view(), name='current-user'),
    url(r'country_list', CountryList.as_view(), name='country-list'),
    url(r'forgot_password', ForgotPassword.as_view(), name='country-list'),
    url(r'create_route', CreateRouteApi.as_view(), name='create-route-api'),
    url(r'route_list/(?P<pk>[a-zA-Z0-9]+)', RouteListApi.as_view(), name='route-list-api'),
    url(r'optimized_route_list/(?P<pk>[a-zA-Z0-9]+)', OptimizedRouteListApi.as_view(), name='optimized-route-list-api'),
    url(r'edit_route/(?P<pk>[a-zA-Z0-9]+)', EditRouteApi.as_view(), name='edit-route-api'),
    url(r'optimized_edit_route/(?P<pk>[a-zA-Z0-9]+)', OptimizedEditRouteApi.as_view(), name='optimized-edit-route-api'),
    url(r'delete_route/(?P<pk>[a-zA-Z0-9]+)', DeleteRouteApi.as_view(), name='delete-route-api'),
   url(r'events', Events.as_view(), name='events-api'),
   url(r'routes_per_day/(?P<pk>[a-zA-Z0-9]+)/(?P<year>[a-zA-Z0-9]+)/(?P<month>[a-zA-Z0-9]+)/(?P<day>[a-zA-Z0-9]+)', RoutesPerDay.as_view(), name='routes-per-day'),


   url(r'^', include(router.urls)),
)
