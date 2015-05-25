import random
import string
from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.core.validators import RegexValidator


class UserProfiles(models.Model):

    user = models.OneToOneField(User, related_name='user_profiles')
    address = models.CharField(max_length=150)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.IntegerField(default=0)
    country = CountryField()
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in format: '+999999999'. Max 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=15)  # validators should be a list
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