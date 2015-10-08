'''
'''
from django import forms

from siteadmin.models import *


class HelpSectionForm(forms.ModelForm):
    class Meta:
        model = HelpSection