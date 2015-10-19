import random
import string
from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.core.validators import RegexValidator
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save,pre_save,pre_delete
from django.dispatch import receiver
from django.utils.translation import ugettext, ugettext_lazy as _

from accounts.constants import *


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class UserProfiles(models.Model):

    ROLES_CHOICES = (
        ('super_admin', 'Super Admin'),
        ('admin', 'Admin'),
        ('employee', 'Employee')
    )

    user = models.OneToOneField(User, related_name='user_profiles')
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=30)
    country = CountryField()
    # phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
    #                              message="Phone number must be entered in format: '+999999999'. Max 15 digits allowed.")
    phone_number = models.CharField(max_length=30)  # validators should be a list
    occupation = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    token = models.CharField('Token', max_length=200, blank=True, null=True)
    admin_status = models.CharField(max_length=50, blank=True, null=True)

    user_role = models.CharField(max_length=50, choices=ROLES_CHOICES, blank=True, null=True)
    admin = models.ForeignKey(User, blank=True, null=True)


    def __unicode__(self):
        return u'%s' % self.user

    def random_key(self):
        alphabet = [c for c in string.letters + string.digits if ord(c) < 128]
        return ''.join([random.choice(alphabet) for x in xrange(30)])

    def save(self, *args, **kwargs):
        super(UserProfiles, self).save(*args, **kwargs)
        if not self.token:
            self.token = self.random_key()
        super(UserProfiles, self).save(*args, ** kwargs)



class RegistratedDevice(models.Model):
    user = models.ForeignKey(User)
    device_token = models.CharField(max_length=300)
    device_type = models.CharField(max_length=100)


class Company(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=300, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    zip_code = models.CharField(max_length=30, null=True, blank=True)
    country = CountryField(null=True, blank=True)

    def __unicode__(self):
        return self.name


class Customer(models.Model):

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    address1 = models.CharField(max_length=400)
    address2 = models.CharField(max_length=400, blank=True, null=True)
    near_by_location = models.CharField(max_length=100, blank=True, null=True)
    near_by_location_lat = models.FloatField(default=0.0)
    near_by_location_lng = models.FloatField(default=0.0)
    country_name = models.CharField(max_length=100)
    country_code = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=30)
    mobile_number = models.CharField(max_length=30)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    token = models.CharField('Token', max_length=200, blank=True, null=True)

    def __unicode__(self):
        return u'%s' % self.user

    def random_key(self):
        alphabet = [c for c in string.letters + string.digits if ord(c) < 128]
        return ''.join([random.choice(alphabet) for x in xrange(30)])

    def save(self, *args, **kwargs):
        super(Customer, self).save(*args, **kwargs)
        if not self.token:
            self.token = self.random_key()
        super(Customer, self).save(*args, ** kwargs)


class Theme(models.Model):
    # logo_url = models.URLField(null=True)
    logo = models.FileField(upload_to='uploads', null=True, blank=True)

    background_color = models.CharField(max_length=10, default=MOBILE_THEME_CONSTANTS['background_color'])

    navigation_color = models.CharField(max_length=10, default=MOBILE_THEME_CONSTANTS['navigation_color'])

    active_button_color = models.CharField(max_length=10, default=MOBILE_THEME_CONSTANTS['active_button_color'])
    active_button_text_color = models.CharField(max_length=10, default=MOBILE_THEME_CONSTANTS['active_button_text_color'])

    inactive_button_color = models.CharField(max_length=10, default=MOBILE_THEME_CONSTANTS['inactive_button_color'])
    inactive_button_text_color = models.CharField(max_length=10, default=MOBILE_THEME_CONSTANTS['inactive_button_text_color'])


class WebTheme(models.Model):
    # logo_url = models.URLField(null=True)
    logo = models.FileField(upload_to='uploads', null=True)

    background_color = models.CharField(max_length=10, default=WEB_THEME_CONSTANTS['background_color'])
    text_color = models.CharField(max_length=10, default=WEB_THEME_CONSTANTS['text_color'])

    header_background_color = models.CharField(max_length=10, default=WEB_THEME_CONSTANTS['header_background_color'])
    header_text_color = models.CharField(max_length=10, default=WEB_THEME_CONSTANTS['header_text_color'])

    menu_background_color = models.CharField(max_length=10, default=WEB_THEME_CONSTANTS['menu_background_color'])
    menu_text_color = models.CharField(max_length=10, default=WEB_THEME_CONSTANTS['menu_text_color'])

    footer_background_color = models.CharField(max_length=10, default=WEB_THEME_CONSTANTS['footer_background_color'])
    footer_text_color = models.CharField(max_length=10, default=WEB_THEME_CONSTANTS['footer_text_color'])

    link_active_color = models.CharField(max_length=10, default=WEB_THEME_CONSTANTS['link_active_color'])
    link_active_hover_color = models.CharField(max_length=10, default=WEB_THEME_CONSTANTS['link_active_hover_color'])
    link_inactive_color = models.CharField(max_length=10, default=WEB_THEME_CONSTANTS['link_inactive_color'])
    link_inactive_hover_color = models.CharField(max_length=10, default=WEB_THEME_CONSTANTS['link_inactive_hover_color'])

    default_button_color = models.CharField(max_length=10, default=WEB_THEME_CONSTANTS['default_button_color'])
    default_button_text_color = models.CharField(max_length=10, default=WEB_THEME_CONSTANTS['default_button_text_color'])
    default_button_border_color = models.CharField(max_length=10, default=WEB_THEME_CONSTANTS['default_button_border_color'])
    default_button_inactive_color = models.CharField(max_length=10, default=WEB_THEME_CONSTANTS['default_button_inactive_color'])
    default_button_inactive_text_color = models.CharField(max_length=10, default=WEB_THEME_CONSTANTS['default_button_inactive_text_color'])
    default_button_inactive_border_color = models.CharField(max_length=10, default=WEB_THEME_CONSTANTS['default_button_inactive_border_color'])

    primary_button_color = models.CharField(max_length=10, default=WEB_THEME_CONSTANTS['primary_button_color'])
    primary_button_text_color = models.CharField(max_length=10, default=WEB_THEME_CONSTANTS['primary_button_text_color'])
    primary_button_border_color = models.CharField(max_length=10, default=WEB_THEME_CONSTANTS['primary_button_border_color'])
    primary_button_inactive_color = models.CharField(max_length=10, default=WEB_THEME_CONSTANTS['primary_button_inactive_color'])
    primary_button_inactive_text_color = models.CharField(max_length=10, default=WEB_THEME_CONSTANTS['primary_button_inactive_text_color'])
    primary_button_inactive_border_color = models.CharField(max_length=10, default=WEB_THEME_CONSTANTS['primary_button_inactive_border_color'])

    error_box_background_color = models.CharField(max_length=10, default=WEB_THEME_CONSTANTS['error_box_background_color'])
    error_text_color = models.CharField(max_length=10, default=WEB_THEME_CONSTANTS['error_text_color'])


class Organization(models.Model):
    super_admin = models.OneToOneField(User, related_name='super_admin_role')
    admins = models.ManyToManyField(User, related_name='admin_role', blank=True, null=True)
    employees = models.ManyToManyField(User, related_name='employee_role', blank=True, null=True)
    theme = models.ForeignKey(Theme, null=True, blank=True, related_name="theme")
    web_theme = models.ForeignKey(WebTheme, null=True, blank=True, related_name="web_theme")


class OrganizationRoles(models.Model):
    role_name = models.CharField(max_length=100, blank=True, null=True)


class CategoryForForm(models.Model):

    STATUS_CHOICES = (
        ('active', 'Activate'),
        ('deactive', 'Deactivate'),
    )

    organization = models.ForeignKey(Organization)
    serial_no = models.IntegerField()
    category_name = models.CharField(max_length=200)
    remarks = models.CharField(max_length=400)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)


class OrgForms(models.Model):

    ASSIGN_ALLOW_CHOICES = (
        ('yes', 'YES'),
        ('no', 'NO'),
    )

    STATUS_CHOICES = (
        ('active', 'Activate'),
        ('deactive', 'Deactivate'),
    )

    form_cat = models.ForeignKey(CategoryForForm, related_name='org_category')
    serial_no = models.IntegerField()
    form_name = models.CharField(max_length=200)
    input_assign_to = models.ManyToManyField(OrganizationRoles, related_name='input_assign', blank=True, null=True)
    display_assign_to = models.ManyToManyField(OrganizationRoles, related_name='display_assign', blank=True, null=True)
    allow_accept_reject = models.CharField(max_length=5, choices=ASSIGN_ALLOW_CHOICES, blank=True, null=True)
    mapped_form = models.ForeignKey("self", blank=True, null=True, related_name='map_form')
    input_assign_allow = models.CharField(max_length=5, choices=ASSIGN_ALLOW_CHOICES, blank=True, null=True)
    display_assign_allow = models.CharField(max_length=5, choices=ASSIGN_ALLOW_CHOICES, blank=True, null=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)


TEXT = 1
TEXTAREA = 2
EMAIL = 3
CHECKBOX_MULTIPLE = 4
SELECT = 5
SELECT_MULTIPLE = 6
RADIO_MULTIPLE = 7
FILE = 8
DATE = 9
DATE_TIME = 10
NUMBER = 12
URL = 11

# Names for all available field types.
NAMES = (
    (TEXT, _("Single line text")),
    (TEXTAREA, _("Multi line text")),
    (EMAIL, _("Email")),
    (NUMBER, _("Number")),
    (URL, _("URL")),
    (CHECKBOX_MULTIPLE, _("Check boxes")),
    (SELECT, _("Drop down")),
    (SELECT_MULTIPLE, _("Multi select")),
    (RADIO_MULTIPLE, _("Radio buttons")),
    (FILE, _("File upload")),
    (DATE, _("Date")),
    (DATE_TIME, _("Date/time")),
)


class FormFields(models.Model):

    org_form = models.ForeignKey(OrgForms, related_name='fields_form')
    label = models.CharField(max_length=100)
    field_type = models.IntegerField(choices=NAMES)
    required = models.BooleanField(default=True)
    choices = models.CharField(max_length=5000, blank=True, null=True)
    placeholder_text = models.CharField(null=True, blank=True, max_length=100)
    is_exist = models.BooleanField(default=True)


class FormEntries(models.Model):

    STATUS_CHOICES = (
        ('need_action', 'Need to take action'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )

    org_form = models.ForeignKey(OrgForms, related_name='entry-org-form')
    customer = models.ForeignKey(Customer, blank=True, null=True)
    org_member = models.ForeignKey(User, blank=True, null=True, related_name='member_name')
    serial_no = models.IntegerField()
    entry_status = models.CharField(max_length=20, choices=STATUS_CHOICES, blank=True, null=True)
    assigned_to = models.ForeignKey(User, blank=True, null=True, related_name='assigned_to_name')
    assigned_by = models.ForeignKey(User, blank=True, null=True, related_name='assigned_by_name')
    mapped_entry = models.ForeignKey("self", blank=True, null=True)


class FormFieldEntries(models.Model):

    form_entry = models.ForeignKey(FormEntries)
    field_id = models.ForeignKey(FormFields)
    text_value = models.CharField(max_length=500, blank=True, null=True)
    email_value = models.EmailField(blank=True, null=True)
    number_value = models.IntegerField(blank=True, null=True)
    url_value = models.URLField(blank=True, null=True)
    datetime_value = models.DateTimeField(blank=True, null=True)
    date_value = models.DateField(blank=True, null=True)
    file_value = models.FileField(blank=True, null=True)
    choice_value = models.CharField(max_length=100, blank=True, null=True)


class SubscriptionDetails(models.Model):
    PLANS = (
        ('monthly', 'Monthly'),
        ('annual', 'Annual')
    )
    TRANSACTION_STATUS = (
        ('processing', 'Processing'),
        ('paid', 'Paid'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    )
    user = models.ForeignKey(User)
    subscription_plan = models.CharField(choices=PLANS, max_length=100)
    subscribed_date = models.DateField()
    expiry_date = models.DateField()
    amount_paid = models.IntegerField()
    payment_id = models.CharField(max_length=150)
    status = models.CharField(choices=TRANSACTION_STATUS, max_length=100)


class CompanyRegistration(models.Model):

    super_admin_id = models.OneToOneField(Organization, related_name='org_registration')
    company_name = models.CharField(max_length=100)
    logo = models.FileField(_('Company Logo'), upload_to='company_logos')
    address1 = models.CharField(max_length=300, blank=True, null=True)
    address2 = models.CharField(max_length=300, blank=True, null=True)
    near_by_location = models.CharField(max_length=500, blank=True, null=True)
    speciality = models.CharField(max_length=500, blank=True, null=True)
    phone1 = models.CharField(max_length=20, blank=True, null=True)
    phone2 = models.CharField(max_length=20, blank=True, null=True)
    email_address1 = models.EmailField()
    email_address2 = models.EmailField()
    about_us = models.CharField(max_length=1000, blank=True, null=True)

    def __unicode__(self):
        return u'%s' % self.company_name


class CustomerCompany(models.Model):
    customer_id = models.ForeignKey(Customer, related_name='customer_follower')
    company_id = models.ForeignKey(CompanyRegistration, related_name='company_followed')

