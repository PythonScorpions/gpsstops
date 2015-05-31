from django import template

register = template.Library()


@register.simple_tag
def retrieve_title(location_address):
    address_list = location_address.split(',')
    return address_list[0]