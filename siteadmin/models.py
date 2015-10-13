'''
'''
from django.db import models
from ckeditor.fields import RichTextField


class HelpSection(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    ref = models.CharField(max_length=300, null=True, blank=True)
    content = RichTextField()
    order_by = models.IntegerField(default=0)
    help_section = models.ForeignKey('HelpSection', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '%s - %s' % (self.title, self.slug)

