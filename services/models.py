from accounts.models import *
from django.utils.translation import ugettext_lazy as _


class ServiceCategory(models.Model):

    super_admin = models.ForeignKey(Organization, related_name='super_admin_service')
    category_name = models.CharField(max_length=300)
    cat_description = models.CharField(max_length=500, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return u'%s' % self.category_name


class ServiceSubCategory(models.Model):

    service_category = models.ForeignKey(ServiceCategory, related_name='service-category')
    subcategory_name = models.CharField(max_length=300)
    sub_cat_description = models.CharField(max_length=500, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return u'%s' % self.subcategory_name


class Services(models.Model):

    service_category = models.ForeignKey(ServiceCategory, related_name='ser-category')
    service_sub_category = models.ForeignKey(ServiceSubCategory, related_name='service-subcategory')
    service_name = models.CharField(max_length=200)
    service_desc1 = models.CharField(max_length=1000)
    service_desc2 = models.CharField(max_length=1000, blank=True, null=True)
    about_service = models.TextField(max_length=5000, blank=True, null=True)
    start_price = models.FloatField(default=0.0)
    end_price = models.FloatField(default=0.0)
    price_info = models.CharField(max_length=200)
    service_image = models.FileField(_('Service Attachment'), upload_to='service_attachments',
                                     blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return u'%s' % self.service_name


class ServiceInquiry(models.Model):

    customer_id = models.ForeignKey(Customer, related_name='customer-ser-inquiry')
    service_id = models.ForeignKey(Services, related_name='ser-inquiry')
    company_id = models.ForeignKey(CompanyRegistration, related_name='company-ser-inquiry')
    note = models.CharField(max_length=1000)
    service_datetime = models.CharField(max_length=100)
    image = models.FileField(upload_to='service_inquiries', blank=True, null=True)
    reply_status = models.BooleanField(default=False)
    accept_status = models.BooleanField(default=False)
    reject_status = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s %s' % self.customer_id, self.service_id


class ServiceInquiryReply(models.Model):

    service_request_id = models.ForeignKey(ServiceInquiry, related_name='inq_reply')
    comments = models.TextField(max_length=1000)

    def __unicode__(self):
        return u'%s %s' % self.comments