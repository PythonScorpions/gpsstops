from accounts.models import *
from django.utils.translation import ugettext_lazy as _


class ProductCategory(models.Model):

    super_admin = models.ForeignKey(Organization, related_name='super_admin_product')
    category_name = models.CharField(max_length=300)
    cat_description = models.CharField(max_length=500, blank=True, null=True)

    def __unicode__(self):
        return u'%s' % self.category_name


class ProductSubCategory(models.Model):

    product_category = models.ForeignKey(ProductCategory, related_name='product-category')
    subcategory_name = models.CharField(max_length=300)
    sub_cat_description = models.CharField(max_length=500, blank=True, null=True)

    def __unicode__(self):
        return u'%s' % self.subcategory_name


class Products(models.Model):

    product_category = models.ForeignKey(ProductCategory, related_name='pro-category')
    product_sub_category = models.ForeignKey(ProductSubCategory, related_name='product-subcategory')
    product_name = models.CharField(max_length=200)
    product_desc1 = models.CharField(max_length=1000)
    product_desc2 = models.CharField(max_length=1000, blank=True, null=True)
    about_product = models.TextField(max_length=5000, blank=True, null=True)
    start_price = models.FloatField(default=0.0)
    end_price = models.FloatField(default=0.0)
    price_info = models.CharField(max_length=200)
    features = models.TextField(max_length=1000, blank=True, null=True)
    specs = models.TextField(max_length=1000, blank=True, null=True)

    def __unicode__(self):
        return u'%s' % self.product_name


class ProductImages(models.Model):

    product = models.ForeignKey(Products, related_name='product-rev')
    product_image = models.FileField(_('Attachment'), upload_to='attachments')