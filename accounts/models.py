import random
import string
from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.core.validators import RegexValidator
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save,pre_save,pre_delete
from django.dispatch import receiver


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
