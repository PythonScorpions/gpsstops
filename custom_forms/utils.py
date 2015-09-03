from accounts.models import *


def retrieve_organization(request, entries_type=None):

    if request.user.user_profiles.user_role == 'admin':
        org_obj = Organization.objects.get(super_admin=request.user.user_profiles.admin)
        if entries_type == 'display':
            display_forms = OrgForms.objects.filter(form_cat__organization=org_obj, display_assign_to__id=3)
            return org_obj, display_forms
        elif entries_type == 'input':
            display_forms = OrgForms.objects.filter(form_cat__organization=org_obj, input_assign_to__id=3)
            return org_obj, display_forms
        else:
            return org_obj
    elif request.user.user_profiles.user_role == 'super_admin':
        org_obj = Organization.objects.get(super_admin__id=request.user.id)
        if entries_type == 'display':
            display_forms = OrgForms.objects.filter(form_cat__organization=org_obj, display_assign_to__id=4)
            return org_obj, display_forms
        elif entries_type == 'input':
            display_forms = OrgForms.objects.filter(form_cat__organization=org_obj, input_assign_to__id=4)
            return org_obj, display_forms
        else:
            return org_obj
    else:
        org_obj = Organization.objects.get(employees=request.user)
        if entries_type == 'display':
            display_forms = OrgForms.objects.filter(form_cat__organization=org_obj, display_assign_to__id=2)
            return org_obj, display_forms
        elif entries_type == 'input':
            display_forms = OrgForms.objects.filter(form_cat__organization=org_obj, input_assign_to__id=2)
            return org_obj, display_forms
        else:
            return org_obj


def retrieve_employees(frm_object, org_obj):

    assign_to_roles = []

    for inp in frm_object.input_assign_to.all():
        if inp.role_name not in assign_to_roles:
            assign_to_roles.append(inp.role_name)
    for dis in frm_object.display_assign_to.all():
        if dis.role_name not in assign_to_roles:
            assign_to_roles.append(dis.role_name)

    if frm_object.map_form.all():
        for mapped_one in frm_object.map_form.all():
            for inp in mapped_one.input_assign_to.all():
                if inp.role_name not in assign_to_roles:
                    assign_to_roles.append(inp.role_name)
            for dis in mapped_one.display_assign_to.all():
                if dis.role_name not in assign_to_roles:
                    assign_to_roles.append(dis.role_name)

    if 'Admin' in assign_to_roles and 'Employee' in assign_to_roles:
        employees = org_obj.employees.all() | org_obj.admins.all()
    elif 'Admin' in assign_to_roles:
        employees = org_obj.admins.all()
    elif 'Employee' in assign_to_roles:
        employees = org_obj.employees.all()
    else:
        employees = []

    return employees