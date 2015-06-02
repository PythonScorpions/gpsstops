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

    user = models.OneToOneField(User, related_name='user_profiles')
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.IntegerField(default=0)
    country = CountryField()
    # phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
    #                              message="Phone number must be entered in format: '+999999999'. Max 15 digits allowed.")
    phone_number = models.CharField(max_length=15)  # validators should be a list
    occupation = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    token = models.CharField('Token', max_length=200, blank=True, null=True)

    def __unicode(self):
        return u'%s' % self.user

    def random_key(self):
        alphabet = [c for c in string.letters + string.digits if ord(c) < 128]
        return ''.join([random.choice(alphabet) for x in xrange(30)])

    def save(self, *args, **kwargs):
        super(UserProfiles, self).save(*args, **kwargs)
        self.token = self.random_key()
        super(UserProfiles, self).save(*args, ** kwargs)