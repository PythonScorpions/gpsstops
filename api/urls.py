'''
'''
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
router.register(r'users', UsersViewSet, base_name='Users')


urlpatterns = patterns("api.views",
    url(r'create_user/$', CreateUser.as_view(), name='create-user'),
    url(r'update_user/(?P<pk>[a-zA-Z0-9]+)$', UpdateUser.as_view(), name='update-user'),
    url(r'^api-token-auth/$', ObtainAuthToken.as_view(), name='token-check'),
    url(r'^device/login/$', GetAuthToken.as_view(), name='token-login-check'),
    url(r'^device/logout/$', LogoutUser.as_view(), name='logout'),
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
    url(r'routes_per_day/(?P<pk>[a-zA-Z0-9]+)/(?P<year>[a-zA-Z0-9]+)/(?P<month>[a-zA-Z0-9]+)/(?P<day>[a-zA-Z0-9]+)',
      RoutesPerDay.as_view(), name='routes-per-day'),

    url(r'^', include(router.urls)),
    url(r'agenda/$', AgendaView.as_view(), name='agendas'),
    url(r'theme/$', ThemeView.as_view(), name='theme_view'),

    url(r'customer_post/$', CustomerPost.as_view(), name='customer-post'),
    url(r'customer_profile/(?P<pk>[a-zA-Z0-9]+)', CustomerProfile.as_view(), name='customer-profile'),
    url(r'customer_update_profile/(?P<pk>[a-zA-Z0-9]+)', CustomerUpdateProfile.as_view(),
        name='customer-update-profile'),
    url(r'customer_login/$', CustomerLogin.as_view(), name='customer-login'),
    url(r'customer_forget_password$', CustomerPassword.as_view(), name='customer-forgot-password'),

    url(r'product_category_post/$', ProCategoryPost.as_view(), name='pro-category-post'),
    url(r'product_category_update/(?P<pk>[a-zA-Z0-9]+)', ProCategoryUpdate.as_view(), name='pro-category-update'),
    url(r'product_category_delete/(?P<pk>[a-zA-Z0-9]+)', ProCategoryDelete.as_view(), name='pro-category-delete'),
    url(r'product_category_list/(?P<pk>[a-zA-Z0-9]+)', ProCategoryList.as_view(), name='pro-category-list'),
    #
    url(r'product_subcategory_post/$', ProSubCategoryPost.as_view(), name='pro-subcategory-post'),
    url(r'product_subcategory_update/(?P<pk>[a-zA-Z0-9]+)', ProSubCategoryUpdate.as_view(),
        name='pro-subcategory-update'),
    url(r'product_subcategory_delete/(?P<pk>[a-zA-Z0-9]+)', ProSubCategoryDelete.as_view(),
        name='pro-subcategory-delete'),
    url(r'product_subcategory_list/(?P<pk>[a-zA-Z0-9]+)', ProSubCategoryList.as_view(), name='pro-subcategory-list'),
    #
    url(r'product_post/$', ProductPost.as_view(), name='product-post'),
    url(r'product_update/(?P<pk>[a-zA-Z0-9]+)', ProductUpdate.as_view(), name='product-update'),
    url(r'product_delete/(?P<pk>[a-zA-Z0-9]+)', ProductDelete.as_view(), name='product-delete'),
    url(r'product_list/(?P<pk>[a-zA-Z0-9]+)', ProductList.as_view(), name='product-list'),
    url(r'product_list_cat/(?P<pk>[a-zA-Z0-9]+)/(?P<key>[a-zA-Z0-9]+)/(?P<val>[a-zA-Z0-9]+)', ProductListCat.as_view(),
        name='product-list-cat'),
    #
    url(r'service_category_post/$', SerCategoryPost.as_view(), name='ser-category-post'),
    url(r'service_category_update/(?P<pk>[a-zA-Z0-9]+)', SerCategoryUpdate.as_view(), name='ser-category-update'),
    url(r'service_category_delete/(?P<pk>[a-zA-Z0-9]+)', SerCategoryDelete.as_view(), name='ser-category-delete'),
    url(r'service_category_list/(?P<pk>[a-zA-Z0-9]+)', SerCategoryList.as_view(), name='ser-category-list'),

    url(r'service_subcategory_post/$', SerSubCategoryPost.as_view(), name='ser-subcategory-post'),
    url(r'service_subcategory_update/(?P<pk>[a-zA-Z0-9]+)', SerSubCategoryUpdate.as_view(),
        name='ser-subcategory-update'),
    url(r'service_subcategory_delete/(?P<pk>[a-zA-Z0-9]+)', SerSubCategoryDelete.as_view(),
        name='ser-subcategory-delete'),
    url(r'service_subcategory_list/(?P<pk>[a-zA-Z0-9]+)', SerSubCategoryList.as_view(), name='ser-subcategory-list'),

    url(r'service_post/$', ServicePost.as_view(), name='service-post'),
    url(r'service_update/(?P<pk>[a-zA-Z0-9]+)', ServiceUpdate.as_view(), name='service-update'),
    url(r'service_delete/(?P<pk>[a-zA-Z0-9]+)', ServiceDelete.as_view(), name='service-delete'),
    url(r'service_list/(?P<pk>[a-zA-Z0-9]+)', ServiceList.as_view(), name='service-list'),
    url(r'service_list_cat/(?P<pk>[a-zA-Z0-9]+)/(?P<key>[a-zA-Z0-9]+)/(?P<val>[a-zA-Z0-9]+)', ServiceListCat.as_view(),
        name='service-list-cat'),

    url(r'company_post/$', CompanyPost.as_view(), name='company-post'),
    url(r'company_details/(?P<pk>[a-zA-Z0-9]+)', CompanyDetails.as_view(), name='company-details'),
    url(r'company_update/(?P<pk>[a-zA-Z0-9]+)', CompanyUpdate.as_view(), name='company-update'),

    url(r'company_follow/$', CompanyFollow.as_view(), name='company-follow'),
    url(r'company_unfollow/$', CompanyUnFollow.as_view(), name='company-unfollow'),

    url(r'all_company_list/(?P<pk>[a-zA-Z0-9]+)', AllCompanyList.as_view(), name='all-company-list'),
    url(r'my_company_list/(?P<pk>[a-zA-Z0-9]+)', MyCompanyList.as_view(), name='my-company-list'),

    url(r'request_product_quote/$', RequestProductQuote.as_view(), name='request-product-quote'),
    url(r'request_service_quote/$', RequestServiceQuote.as_view(), name='request-service-quote'),
    url(r'request_product_details/(?P<pk>[a-zA-Z0-9]+)', RequestProductDetails.as_view(),
        name='request-product-details'),
    url(r'request_service_details/(?P<pk>[a-zA-Z0-9]+)', RequestServiceDetails.as_view(),
        name='request-service-details'),
    url(r'answer_product_quote/$', AnswerProductQuote.as_view(), name='answer-product-quote'),
    url(r'answer_service_quote/$', AnswerServiceQuote.as_view(), name='answer-service-quote'),

    url(r'quotes_list/(?P<pk>[a-zA-Z0-9]+)/(?P<key>[a-zA-Z0-9]+)', QuotesList.as_view(),
        name='all-quotes-list'),

    url(r'quote_answer/(?P<pk>[a-zA-Z0-9]+)/(?P<key>[a-zA-Z0-9]+)', QuoteAnswer.as_view(),
        name='all-quotes-list'),
)