from django import template

register = template.Library()


# @register.simple_tag
@register.filter(name='cho')
def split_strip_choices(value):
    return value.replace(" ", "").split(',')


@register.filter(name='roles')
def retrieve_roles_list(value):
    return [role.role_name for role in value]