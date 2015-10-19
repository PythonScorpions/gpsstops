from django.conf.urls import patterns, include, url
from services.views import *


urlpatterns = patterns("services.views",
                       url(r'category', SerCategory.as_view(), name='ser-category'),
                       url(r'add_cat', CategoryAdd.as_view(), name='ser-category-add'),
                       url(r'edit_cat/(?P<pk>\d+)$', CategoryAdd.as_view(), name='ser-category-edit'),
                       url(r'delete_cat/(?P<key>\d+)$', CategoryAdd.as_view(), name='ser-category-delete'),

                       url(r'subcat', SerSubCat.as_view(), name='ser-subcat'),
                       url(r'catesub_add', SubCategoryAdd.as_view(), name='ser-catesub_add'),
                       url(r'edit_catesub/(?P<pk>\d+)$', SubCategoryAdd.as_view(), name='ser-subcategory_edit'),
                       url(r'delete_catesub/(?P<key>\d+)$', SubCategoryAdd.as_view(), name='ser-subcategory_delete'),

                       url(r'service-list', SerList.as_view(), name='ser-list'),
                       url(r'service_add', ServiceAdd.as_view(), name='service-add'),
                       url(r'edit_ser/(?P<pk>\d+)$', ServiceAdd.as_view(), name='service-edit'),
                       url(r'delete_ser/(?P<key>\d+)$', ServiceAdd.as_view(), name='service-delete'),

                       url(r'service-inquiries', SerInquiries.as_view(), name='ser-inquiry'),
                       url(r'service_inquiries_view/(?P<pk>\d+)$', SerInquiriesView.as_view(), name='ser-inquiry-view'),
                       url(r'service_inquiry_status/(?P<pk>\d+)/(?P<key>\d+)$', SerInquiryStatus.as_view(),
                           name='ser-inquiry-status'),
                       url(r'service_inquiry_reply/(?P<pk>\d+)$', SerInquiryReply.as_view(), name='ser-inquiry-reply'),

                       url('^all_suboptions', all_suboptions)
                       )