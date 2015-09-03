from django.conf.urls import patterns, include, url
from custom_forms.views import *

urlpatterns = patterns("custom_forms.views",
                       url(r'form_category$', FormCategory.as_view(), name='form-category'),
                       url(r'form_category/edit/(?P<pk>\d+)$', FormCategory.as_view(), name='form-category-edit'),
                       url(r'change_status/(?P<key>\d+)$', FormCategory.as_view(), name='form-category-status'),

                       url(r'forms_created', FormsCreated.as_view(), name='forms-created'),
                       url(r'change_form_status/(?P<pk>\d+)$', ChangeFormStatus.as_view(), name='change-form-status'),
                       url(r'create_form', FormAdd.as_view(), name='form-add'),
                       url(r'edit_form/(?P<pk>\d+)', FormEdit.as_view(), name='form-edit'),
                       url(r'customers', CustomerData.as_view(), name='customers'),
                       url(r'customer_forms/(?P<pk>\d+)$', CustomerFormsData.as_view(), name='customer-forms'),
                       url(r'customer_into_form/(?P<pk>\d+)/(?P<key>\d+)$', CustomerFormFields.as_view(),
                           name='customer-form-fields'),

                       url(r'display_forms', DisplayForms.as_view(), name='display-forms'),
                       url(r'input_forms', InputForms.as_view(), name='input-forms'),
                       url(r'display_form_entries/(?P<pk>\d+)$', DisplayFormEntries.as_view(),
                           name='display-form-entries'),
                       url(r'view_form_entry/(?P<pk>\d+)$', ViewFormEntry.as_view(),
                           name='view-form-entry'),
                       url(r'edit_form_entry/(?P<pk>\d+)$', EditFormEntry.as_view(),
                           name='edit-form-entry'),

                       url(r'org_into_form/(?P<pk>\d+)$', OrgFormFields.as_view(),
                           name='org-form-fields'),
                       url(r'org_into_form/(?P<pk>\d+)/(?P<key>\d+)$', OrgFormFields.as_view(),
                           name='org-form-fields'),
                       )