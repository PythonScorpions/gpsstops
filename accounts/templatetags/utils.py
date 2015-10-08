'''
'''
from django import template

from accounts.models import *


register = template.Library()

@register.filter
def logo(user): # Only one argument.
    organization = None
    try:
        if user.user_profiles.user_role == "super_admin":
            organization = Organization.objects.get(super_admin=user)
        elif user.user_profiles.user_role == "admin":
            organization = Organization.objects.get(admins=user)
        elif user.user_profiles.user_role == "employee":
            organization = Organization.objects.get(employees=user)
    except:
        pass

    # print organization.web_theme.logo
    if organization == None or organization.web_theme == None or not organization.web_theme.logo:
        return '/static/images/theme/logo.jpg'
    return '/media/' + organization.web_theme.logo.name