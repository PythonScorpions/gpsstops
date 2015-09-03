from django import template

register = template.Library()


# @register.simple_tag
@register.filter(name='cho')
def split_strip_choices(value):
    return value.replace(" ", "").split(',')


@register.filter(name='roles')
def retrieve_roles_list(value):
    return [role.role_name for role in value]


@register.filter(name='exist_fields')
def retrieve_existing_fields(value):

    return [val for val in value if val.is_exist]


@register.filter(name='filetypecheck')
def file_type_check(value):

    if str(value).split('.')[-1] == 'png' or str(value).split('.')[-1] == 'jpg' or str(value).split('.')[-1] == 'jpeg':
        return True
    else:
        return False