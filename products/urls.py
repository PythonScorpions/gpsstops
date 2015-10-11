from django.conf.urls import patterns, include, url
from products.views import *


urlpatterns = patterns("products.views",
                       url(r'category', ProCategory.as_view(), name='pro-category'),
                       url(r'add_cat', CategoryAdd.as_view(), name='category-add'),
                       url(r'edit_cat/(?P<pk>\d+)$', CategoryAdd.as_view(), name='category-edit'),
                       url(r'delete_cat/(?P<key>\d+)$', CategoryAdd.as_view(), name='category-delete'),

                       url(r'subcat', ProSubCat.as_view(), name='pro-subcat'),
                       url(r'catesub_add', SubCategoryAdd.as_view(), name='catesub_add'),
                       url(r'edit_catesub/(?P<pk>\d+)$', SubCategoryAdd.as_view(), name='subcategory_edit'),
                       url(r'delete_catesub/(?P<key>\d+)$', SubCategoryAdd.as_view(), name='subcategory_delete'),

                       url(r'product-list', ProList.as_view(), name='pro-list'),
                       url(r'product_add', ProductAdd.as_view(), name='product-add'),
                       url(r'edit_pro/(?P<pk>\d+)$', ProductAdd.as_view(), name='product-edit'),
                       url(r'delete_pro/(?P<key>\d+)$', ProductAdd.as_view(), name='product-delete'),

                       url('^all_suboptions', all_suboptions),
                       url('^delete_image', delete_image),
                       )