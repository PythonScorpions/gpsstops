from django.shortcuts import render_to_response
from django.views.generic import View
from maps.views import custom_login_required
from django.utils.decorators import method_decorator
from django.template import RequestContext
from accounts.forms import *
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from collections import defaultdict
import datetime
from gpsstops import settings


class FormCategory(View):
    template_name = 'custom_forms/form_category.html'
    # form_class = ProfileUpdateForm

    @method_decorator(custom_login_required)
    def get(self, request, pk=None, key=None, *args, **kwargs):

        if pk:
            cat_obj = CategoryForForm.objects.get(id=int(pk))
            initial_data = {
                'category_name': cat_obj.category_name,
                'remarks': cat_obj.remarks,
            }
            form = CategoryForm(instance=cat_obj, initial=initial_data)
            new_serial_no = cat_obj.serial_no
        elif key:
            cat_obj = CategoryForForm.objects.get(id=int(key))
            if cat_obj.status == 'active':
                cat_obj.status = 'deactive'
                cat_obj.save()
            else:
                cat_obj.status = 'active'
                cat_obj.save()
            form = CategoryForm()
            try:
                last_serial_no = CategoryForForm.objects.latest('id').serial_no
                new_serial_no = last_serial_no + 1
            except:
                new_serial_no = 1
        else:
            form = CategoryForm()
            try:
                last_serial_no = CategoryForForm.objects.latest('id').serial_no
                new_serial_no = last_serial_no + 1
            except:
                new_serial_no = 1
        if request.user.user_profiles.user_role == 'admin':
            org_obj = Organization.objects.get(super_admin=request.user.user_profiles.admin)
        else:
            org_obj = Organization.objects.get(super_admin__id=request.user.id)
        categories = CategoryForForm.objects.filter(organization=org_obj)

        return render_to_response(self.template_name, {'form': form, 'serial_no': new_serial_no,
                                                       'categories': categories},
                                  context_instance=RequestContext(request),)

    @method_decorator(custom_login_required)
    def post(self, request, pk=None, key=None, *args, **kwargs):
        print "yes coming here"

        try:
            last_serial_no = CategoryForForm.objects.latest('id').serial_no
            new_serial_no = last_serial_no + 1
        except:
            new_serial_no = 1

        if request.user.user_profiles.user_role == 'admin':
            org_obj = Organization.objects.get(super_admin=request.user.user_profiles.admin)
        else:
            org_obj = Organization.objects.get(super_admin__id=request.user.id)

        categories = CategoryForForm.objects.filter(organization=org_obj)

        if pk:
            cat_obj = CategoryForForm.objects.get(id=int(pk))
            form = CategoryForm(data=request.POST, instance=cat_obj)
        else:
            form = CategoryForm(data=request.POST)

        if form.is_valid():
            if pk:
                cat_obj.category_name = form.cleaned_data['category_name']
                cat_obj.remarks = form.cleaned_data['remarks']
                cat_obj.save()
            else:
                new_category = CategoryForForm(category_name=form.cleaned_data['category_name'],
                                               remarks=form.cleaned_data['remarks'],
                                               organization=org_obj, status='active', serial_no=new_serial_no)
                new_category.save()
        else:
            print form.errors

        return render_to_response(self.template_name, {'form': form, 'serial_no': new_serial_no, 'categories': categories},
                                  context_instance=RequestContext(request),)


class FormsCreated(View):
    template_name = 'custom_forms/forms_created.html'
    # form_class = ProfileUpdateForm

    @method_decorator(custom_login_required)
    def get(self, request, pk=None, key=None, *args, **kwargs):

        if request.user.user_profiles.user_role == 'admin':
            org_obj = Organization.objects.get(super_admin=request.user.user_profiles.admin)
        else:
            org_obj = Organization.objects.get(super_admin__id=request.user.id)
        organization_forms = OrgForms.objects.filter(form_cat__organization=org_obj)

        return render_to_response(self.template_name, {'org_forms': organization_forms},
                                  context_instance=RequestContext(request),)

    @method_decorator(custom_login_required)
    def post(self, request, pk=None, key=None, *args, **kwargs):

        return render_to_response(self.template_name,
                                  context_instance=RequestContext(request),)


class FormAdd(View):
    template1 = 'custom_forms/form_add.html'
    template2 = 'custom_forms/forms_created.html'
    # form_class = ProfileUpdateForm

    @method_decorator(custom_login_required)
    def get(self, request, pk=None, key=None, *args, **kwargs):

        try:
            last_serial_no = OrgForms.objects.latest('id').serial_no
            new_serial_no = last_serial_no + 1
        except:
            new_serial_no = 1
        if request.user.user_profiles.user_role == 'admin':
            org_obj = Organization.objects.get(super_admin=request.user.user_profiles.admin)
        else:
            org_obj = Organization.objects.get(super_admin__id=request.user.id)
        # form = FormForOrgForm(user=request.user)
        cat_choices = []
        for cat in CategoryForForm.objects.filter(organization=org_obj):
            cat_choices.append({'id': cat.id, 'name': cat.category_name})
        map_form_choices = [{'id': 0, 'name': 'None'}]
        for form_obj in OrgForms.objects.filter(form_cat__organization=org_obj):
            map_form_choices.append({'id': form_obj.id, 'name': form_obj.form_name})
        return render_to_response(self.template1, {'serial_no': new_serial_no, 'cat_choices': cat_choices,
                                                   'map_form_choices': map_form_choices},
                                  context_instance=RequestContext(request),)

    @method_decorator(custom_login_required)
    def post(self, request, pk=None, key=None, *args, **kwargs):

        try:
            last_serial_no = OrgForms.objects.latest('id').serial_no
            new_serial_no = last_serial_no + 1
        except:
            new_serial_no = 1

        form_cat_obj = CategoryForForm.objects.get(id=int(request.POST['form_cat']))
        form_name = request.POST['form_name']
        obj_form = OrgForms(form_cat=form_cat_obj, serial_no=new_serial_no, form_name=form_name,
                            allow_accept_reject=request.POST['accept_reject'],
                            input_assign_allow=request.POST['input_assign_allow'],
                            display_assign_allow=request.POST['display_assign_allow'], status='active')
        if request.POST['mapped_form'] != '0':
            obj_form.mapped_form = OrgForms.objects.get(id=int(request.POST['mapped_form']))
        obj_form.save()
        for input_assign in request.POST.getlist('input_assign_to'):
            role_obj = OrganizationRoles.objects.get(id=int(input_assign))
            obj_form.input_assign_to.add(role_obj)

        for display_assign in request.POST.getlist('display_assign_to'):
            role_obj = OrganizationRoles.objects.get(id=int(display_assign))
            obj_form.display_assign_to.add(role_obj)

        field_labels = request.POST.getlist('field_label')
        field_types = request.POST.getlist('field_type')
        choices = request.POST.getlist('choices')
        placeholders = request.POST.getlist('placeholder')

        print field_labels
        print field_types
        print choices
        print placeholders

        for i, (label, ftype, choice, placeholder) in enumerate(zip(field_labels, field_types, choices, placeholders), 1):
            print "coming here"
            required = 'required'+`i`
            try:
                temp = request.POST[required]
                req = True
            except:
                req = False
            FormFields(org_form=obj_form, label=label, field_type=ftype, required=req, choices=choice,
                       placeholder_text=placeholder).save()

        return HttpResponseRedirect(reverse('forms-created'))


class FormEdit(View):
    template1 = 'custom_forms/form_edit.html'
    # form_class = ProfileUpdateForm

    @method_decorator(custom_login_required)
    def get(self, request, pk=None, key=None, *args, **kwargs):

        org_form = OrgForms.objects.get(id=int(pk))

        if request.user.user_profiles.user_role == 'admin':
            org_obj = Organization.objects.get(super_admin=request.user.user_profiles.admin)
        else:
            org_obj = Organization.objects.get(super_admin__id=request.user.id)
        # form = FormForOrgForm(user=request.user)
        cat_choices = []
        for cat in CategoryForForm.objects.filter(organization=org_obj):
            cat_choices.append({'id': cat.id, 'name': cat.category_name})
        map_form_choices = [{'id': 0, 'name': 'None'}]
        for form_obj in OrgForms.objects.filter(form_cat__organization=org_obj):
            map_form_choices.append({'id': form_obj.id, 'name': form_obj.form_name})
        return render_to_response(self.template1, {'org_form': org_form, 'cat_choices': cat_choices,
                                                   'map_form_choices': map_form_choices},
                                  context_instance=RequestContext(request),)


class CustomerData(View):
    template1 = 'custom_forms/customers.html'
    # form_class = ProfileUpdateForm

    @method_decorator(custom_login_required)
    def get(self, request, pk=None, key=None, *args, **kwargs):

        customers = Customer.objects.all()

        return render_to_response(self.template1, {'customers': customers},
                                  context_instance=RequestContext(request),)


class CustomerFormsData(View):
    template1 = 'custom_forms/customer_forms.html'
    # form_class = ProfileUpdateForm

    @method_decorator(custom_login_required)
    def get(self, request, pk=None, *args, **kwargs):

        customer_inputs = OrganizationRoles.objects.get(role_name='Customer').input_assign.all()
        forms_by_category = defaultdict(list)
        for cust_input in customer_inputs:
            forms_by_category[cust_input.form_cat.category_name].append(cust_input)
        return render_to_response(self.template1, {'forms_by_category': dict(forms_by_category), 'customer_id': pk},
                                  context_instance=RequestContext(request),)


class CustomerFormFields(View):
    template1 = 'custom_forms/customer_form_entry.html'
    # form_class = ProfileUpdateForm

    """ pk = customer_id , key = form_id"""
    @method_decorator(custom_login_required)
    def get(self, request, pk=None, key=None, *args, **kwargs):

        try:
            last_serial_no = FormEntries.objects.filter(org_form__id=int(key)).latest('id').serial_no
            new_serial_no = last_serial_no + 1
        except:
            new_serial_no = 1

        form_fields = FormFields.objects.filter(org_form__id=int(key))

        normal_fields = [1, 2, 3, 5, 6, 8, 9, 10, 11, 12]
        choice_fields = [4, 7]
        date_pickers = []
        datetime_pickers = []
        required_normal_fields = []
        required_choice_fields = []
        for i, field in enumerate(form_fields):
            if field.field_type == 9:
                date_pickers.append(i)
            if field.field_type == 10:
                datetime_pickers.append(i)
            if field.required and field.field_type in normal_fields:
                required_normal_fields.append(i)
            if field.required and field.field_type in choice_fields:
                required_choice_fields.append(i)
        return render_to_response(self.template1, {'customer_id': pk, 'form_fields': form_fields,
                                                   'serial_no': new_serial_no,
                                                   'date_pickers': date_pickers, 'datetime_pickers': datetime_pickers,
                                                   'required_normal_fields': required_normal_fields,
                                                   'required_choice_fields': required_choice_fields,
                                                   'normal_fields': normal_fields, 'choice_fields': choice_fields},
                                  context_instance=RequestContext(request),)


    @method_decorator(custom_login_required)
    def post(self, request, pk=None, key=None, *args, **kwargs):

        org_form_obj = OrgForms.objects.get(id=int(key))
        customer = Customer.objects.get(id=int(pk))
        try:
            last_serial_no = FormEntries.objects.filter(org_form__id=int(key)).latest('id').serial_no
            new_serial_no = last_serial_no + 1
        except:
            new_serial_no = 1

        if org_form_obj.allow_accept_reject == 'yes':
            entry_status = 'need_action'
        else:
            entry_status = ''

        form_entry_data = FormEntries(org_form=org_form_obj, customer=customer, serial_no=new_serial_no,
                                      entry_status=entry_status)
        form_entry_data.save()

        form_fields = FormFields.objects.filter(org_form__id=int(key))

        for i, field in enumerate(form_fields):
            field_val = 'field_value'+str(i)

            if field.field_type in [1, 2, 5, 7]:
                try:
                    field_posted_val = request.POST[field_val]
                except:
                    field_posted_val = ''
                FormFieldEntries(form_entry=form_entry_data, field_id=field, text_value=field_posted_val).save()
            if field.field_type == 3:
                try:
                    field_posted_val = request.POST[field_val]
                except:
                    field_posted_val = ''
                FormFieldEntries(form_entry=form_entry_data, field_id=field, email_value=field_posted_val).save()
            if field.field_type in [4, 6]:
                try:
                    field_posted_val = ','.join(request.POST.getlist(field_val))
                except:
                    field_posted_val = ''
                FormFieldEntries(form_entry=form_entry_data, field_id=field, choice_value=field_posted_val).save()
            if field.field_type == 8:
                try:
                    field_posted_val = request.FILES[field_val]
                except:
                    field_posted_val = ''
                FormFieldEntries(form_entry=form_entry_data, field_id=field, file_value=field_posted_val).save()
            if field.field_type == 11:
                try:
                    field_posted_val = request.POST[field_val]
                except:
                    field_posted_val = ''
                FormFieldEntries(form_entry=form_entry_data, field_id=field, url_value=field_posted_val).save()
            if field.field_type == 12:
                try:
                    field_posted_val = request.POST[field_val]
                except:
                    field_posted_val = ''
                FormFieldEntries(form_entry=form_entry_data, field_id=field, number_value=field_posted_val).save()
            if field.field_type == 9:
                try:
                    field_posted_val = datetime.datetime.strptime(str(request.POST[field_val]), "%b %d,%Y").date()
                except:
                    field_posted_val = ''
                FormFieldEntries(form_entry=form_entry_data, field_id=field, date_value=field_posted_val).save()
            if field.field_type == 10:
                try:
                    field_posted_val = datetime.datetime.strptime(str(request.POST[field_val]), "%b %d,%Y %I:%M %p")
                except:
                    field_posted_val = ''
                FormFieldEntries(form_entry=form_entry_data, field_id=field, datetime_value=field_posted_val).save()
        return HttpResponseRedirect(reverse('customer-forms', kwargs={'pk': pk}))


class DisplayForms(View):
    template_name = 'custom_forms/display_forms.html'
    # form_class = ProfileUpdateForm

    @method_decorator(custom_login_required)
    def get(self, request, *args, **kwargs):

        if request.user.user_profiles.user_role == 'admin':
            print "yes it is admin who is logged in"
            org_obj = Organization.objects.get(super_admin=request.user.user_profiles.admin)
            display_forms = OrgForms.objects.filter(form_cat__organization=org_obj, display_assign_to__id=3)
        elif request.user.user_profiles.user_role == 'super_admin':
            print "yes it is super admin who is logged in"
            org_obj = Organization.objects.get(super_admin__id=request.user.id)
            display_forms = OrgForms.objects.filter(form_cat__organization=org_obj, display_assign_to__id=4)
        else:
            print "yes it is employee who is logged in"
            org_obj = Organization.objects.get(employees=request.user)
            display_forms = OrgForms.objects.filter(form_cat__organization=org_obj, display_assign_to__id=2)

        forms_by_category = defaultdict(list)
        for frm in display_forms:
            forms_by_category[frm.form_cat.category_name].append(frm)
        return render_to_response(self.template_name, {'forms_by_category': dict(forms_by_category)},
                                  context_instance=RequestContext(request),)


class DisplayFormEntries(View):
    template_name = 'custom_forms/display_form_entries.html'
    # form_class = ProfileUpdateForm

    @method_decorator(custom_login_required)
    def get(self, request, pk=None, *args, **kwargs):

        temp_form_object = OrgForms.objects.get(id=int(pk))

        if temp_form_object.mapped_form:
            form_object = temp_form_object.mapped_form
            map_frm = True
            map_from_name = temp_form_object.form_name
        elif temp_form_object.map_form.all():
            form_object = temp_form_object
            map_frm = True
            map_from_name = temp_form_object.map_form.all()[0].form_name
        else:
            form_object = temp_form_object
            map_frm = False
            map_from_name = ''

        field_labels = [fld.label for fld in FormFields.objects.filter(org_form__id=int(pk))]

        final_result = {}
        for entry in FormEntries.objects.filter(org_form=form_object):
            temp = []
            for field_entry in FormFieldEntries.objects.filter(form_entry=entry):
                if field_entry.field_id.field_type in [1, 2, 5, 7]:
                    temp.append(field_entry.text_value)
                if field_entry.field_id.field_type in [4, 6]:
                    temp.append(field_entry.choice_value)
                if field_entry.field_id.field_type == 3:
                    temp.append(field_entry.email_value)
                if field_entry.field_id.field_type == 8:
                    temp.append(str(field_entry.file_value))
                if field_entry.field_id.field_type == 11:
                    temp.append(field_entry.url_value)
                if field_entry.field_id.field_type == 12:
                    temp.append(field_entry.number_value)
                if field_entry.field_id.field_type == 9:
                    temp.append(field_entry.date_value)
                if field_entry.field_id.field_type == 10:
                    temp.append(field_entry.datetime_value)
            if form_object.allow_accept_reject == 'yes':
                temp.append(entry.get_entry_status_display())
            if form_object.display_assign_allow == 'yes' or form_object.input_assign_allow == 'yes':
                if entry.assigned_to:
                    temp.append(entry.assigned_to.first_name)
                    temp.append(entry.assigned_by.first_name)
                else:
                    temp.append(None)
                    temp.append(None)
            temp.append(entry.id)
            final_result[entry.serial_no] = temp

        print final_result
        return render_to_response(self.template_name, {'field_labels': field_labels, 'form_object': form_object,
                                                       'final_result': final_result, 'map_frm': map_frm,
                                                       'map_from_name': map_from_name},
                                  context_instance=RequestContext(request),)


class ViewFormEntry(View):
    template_name = 'custom_forms/view_form_entry.html'
    # form_class = ProfileUpdateForm

    @method_decorator(custom_login_required)
    def get(self, request, pk=None, *args, **kwargs):

        field_entries = FormFieldEntries.objects.filter(form_entry__id=int(pk))

        server_url = settings.SERVER_URL

        # For Assign to Field
        if request.user.user_profiles.user_role == 'admin':
            print "yes it is admin who is logged in"
            org_obj = Organization.objects.get(super_admin=request.user.user_profiles.admin)
        elif request.user.user_profiles.user_role == 'super_admin':
            print "yes it is super admin who is logged in"
            org_obj = Organization.objects.get(super_admin__id=request.user.id)
        else:
            print "yes it is employee who is logged in"
            org_obj = Organization.objects.get(employees=request.user)

        employees = org_obj.employees.all()
        print employees

        if field_entries[0].field_id.org_form.map_form.all():
            print True
            mapped_form_entries = FormEntries.objects.filter(mapped_entry__id=int(pk))
            field_labels = [fld.label for fld in FormFields.objects.filter(org_form=mapped_form_entries[0].org_form)]
            print field_labels
            final_result = {}
            for entry in mapped_form_entries:
                temp = []
                for field_entry in FormFieldEntries.objects.filter(form_entry=entry):
                    if field_entry.field_id.field_type in [1, 2, 5, 7]:
                        temp.append(field_entry.text_value)
                    if field_entry.field_id.field_type in [4, 6]:
                        temp.append(field_entry.choice_value)
                    if field_entry.field_id.field_type == 3:
                        temp.append(field_entry.email_value)
                    if field_entry.field_id.field_type == 8:
                        temp.append(str(field_entry.file_value))
                    if field_entry.field_id.field_type == 11:
                        temp.append(field_entry.url_value)
                    if field_entry.field_id.field_type == 12:
                        temp.append(field_entry.number_value)
                    if field_entry.field_id.field_type == 9:
                        temp.append(field_entry.date_value)
                    if field_entry.field_id.field_type == 10:
                        temp.append(field_entry.datetime_value)
                temp.append(entry.id)
                final_result[entry.serial_no] = temp

        else:
            field_labels = []
            final_result = []
        return render_to_response(self.template_name, {'field_entries': field_entries, 'server_url': server_url,
                                                       'employees': employees, 'field_labels': field_labels,
                                                       'final_result': final_result},
                                  context_instance=RequestContext(request),)

    def post(self, request, pk=None, *args, **kwargs):

        frm_object = FormEntries.objects.get(id=int(pk))
        try:
            assign_to_id = request.POST['assign_to']
            frm_object.assigned_to = User.objects.get(id=int(assign_to_id))
            frm_object.assigned_by = request.user
            frm_object.save()
        except:
            pass

        return HttpResponseRedirect(reverse('display-form-entries',
                                            kwargs={'pk': frm_object.obj_form.id}))


class EditFormEntry(View):
    template1 = 'custom_forms/edit_form_entry.html'
    # form_class = ProfileUpdateForm

    @method_decorator(custom_login_required)
    def get(self, request, pk=None, *args, **kwargs):

        field_entries = FormFieldEntries.objects.filter(form_entry__id=int(pk))

        server_url = settings.SERVER_URL

        normal_fields = [1, 2, 3, 5, 6, 9, 10, 11, 12]
        choice_fields = [4, 7]
        date_pickers = []
        datetime_pickers = []
        required_normal_fields = []
        required_choice_fields = []
        for i, entry in enumerate(field_entries):
            if entry.field_id.field_type == 9:
                date_pickers.append(i)
            if entry.field_id.field_type == 10:
                datetime_pickers.append(i)
            if entry.field_id.required and entry.field_id.field_type in normal_fields:
                required_normal_fields.append(i)
            if entry.field_id.required and entry.field_id.field_type in choice_fields:
                required_choice_fields.append(i)

        # For Assign to Field
        if request.user.user_profiles.user_role == 'admin':
            print "yes it is admin who is logged in"
            org_obj = Organization.objects.get(super_admin=request.user.user_profiles.admin)
        elif request.user.user_profiles.user_role == 'super_admin':
            print "yes it is super admin who is logged in"
            org_obj = Organization.objects.get(super_admin__id=request.user.id)
        else:
            print "yes it is employee who is logged in"
            org_obj = Organization.objects.get(employees=request.user)

        frm_object = field_entries[0].form_entry.org_form

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

        return render_to_response(self.template1, {'field_entries': field_entries, 'server_url': server_url,
                                                   'date_pickers': date_pickers, 'datetime_pickers': datetime_pickers,
                                                   'required_normal_fields': required_normal_fields,
                                                   'required_choice_fields': required_choice_fields,
                                                   'normal_fields': normal_fields, 'choice_fields': choice_fields,
                                                   'employees': employees},
                                  context_instance=RequestContext(request),)


    @method_decorator(custom_login_required)
    def post(self, request, pk=None, key=None, *args, **kwargs):

        print "yes coming here"

        field_entries = FormFieldEntries.objects.filter(form_entry__id=int(pk))

        for i, entry in enumerate(field_entries):
            field_val = 'field_value'+str(i)

            if entry.field_id.field_type in [1, 2, 5, 7]:
                try:
                    field_posted_val = request.POST[field_val]
                except:
                    field_posted_val = ''
                entry.text_value = field_posted_val
                entry.save()

            if entry.field_id.field_type == 3:
                try:
                    field_posted_val = request.POST[field_val]
                except:
                    field_posted_val = ''
                entry.email_value = field_posted_val
                entry.save()

            if entry.field_id.field_type in [4, 6]:
                try:
                    field_posted_val = ','.join(request.POST.getlist(field_val))
                except:
                    field_posted_val = ''
                entry.choice_value = field_posted_val
                entry.save()

            if entry.field_id.field_type == 8:
                try:
                    field_posted_val = request.FILES[field_val]
                    entry.file_value = field_posted_val
                    entry.save()
                except:
                    pass

            if entry.field_id.field_type == 11:
                try:
                    field_posted_val = request.POST[field_val]
                except:
                    field_posted_val = ''
                entry.url_value = field_posted_val
                entry.save()

            if entry.field_id.field_type == 12:
                try:
                    field_posted_val = request.POST[field_val]
                except:
                    field_posted_val = ''
                entry.number_value = field_posted_val
                entry.save()

            if entry.field_id.field_type == 9:
                try:
                    field_posted_val = datetime.datetime.strptime(str(request.POST[field_val]), "%b %d,%Y").date()
                except:
                    field_posted_val = ''
                entry.date_value = field_posted_val
                entry.save()

            if entry.field_id.field_type == 10:
                try:
                    field_posted_val = datetime.datetime.strptime(str(request.POST[field_val]), "%b %d,%Y %I:%M %p")
                except:
                    field_posted_val = ''
                entry.datetime_value = field_posted_val
                entry.save()

        try:
            action = request.POST['approve_reject']
            frm_object = FormEntries.objects.get(id=int(pk))
            frm_object.entry_status = action
            frm_object.save()
        except:
            pass

        try:
            assign_to_id = request.POST['assign_to']
            frm_object = FormEntries.objects.get(id=int(pk))
            frm_object.assigned_to = User.objects.get(id=int(assign_to_id))
            frm_object.assigned_by = request.user
            frm_object.save()
        except:
            pass

        return HttpResponseRedirect(reverse('display-form-entries',
                                            kwargs={'pk': field_entries[0].form_entry.org_form.id}))


class InputForms(View):
    template_name = 'custom_forms/input_forms.html'
    # form_class = ProfileUpdateForm

    @method_decorator(custom_login_required)
    def get(self, request, *args, **kwargs):

        if request.user.user_profiles.user_role == 'admin':
            print "yes it is admin who is logged in"
            org_obj = Organization.objects.get(super_admin=request.user.user_profiles.admin)
            display_forms = OrgForms.objects.filter(form_cat__organization=org_obj, input_assign_to__id=3)
        elif request.user.user_profiles.user_role == 'super_admin':
            print "yes it is super admin who is logged in"
            org_obj = Organization.objects.get(super_admin__id=request.user.id)
            display_forms = OrgForms.objects.filter(form_cat__organization=org_obj, input_assign_to__id=4)
        else:
            print "yes it is employee who is logged in"
            org_obj = Organization.objects.get(employees=request.user)
            display_forms = OrgForms.objects.filter(form_cat__organization=org_obj, input_assign_to__id=2)

        forms_by_category = defaultdict(list)
        for frm in display_forms:
            forms_by_category[frm.form_cat.category_name].append(frm)
        return render_to_response(self.template_name, {'forms_by_category': dict(forms_by_category)},
                                  context_instance=RequestContext(request),)


class OrgFormFields(View):
    template1 = 'custom_forms/org_form_entry.html'

    @method_decorator(custom_login_required)
    def get(self, request, pk=None, key=None, *args, **kwargs):

        print "------------------------------------------------------------", key

        try:
            last_serial_no = FormEntries.objects.filter(org_form__id=int(pk)).latest('id').serial_no
            new_serial_no = last_serial_no + 1
        except:
            new_serial_no = 1

        form_fields = FormFields.objects.filter(org_form__id=int(pk))

        if key:
            field_entries = FormFieldEntries.objects.filter(form_entry__id=int(key))
        else:
            field_entries = []

        server_url = settings.SERVER_URL

        normal_fields = [1, 2, 3, 5, 6, 8, 9, 10, 11, 12]
        choice_fields = [4, 7]
        date_pickers = []
        datetime_pickers = []
        required_normal_fields = []
        required_choice_fields = []
        for i, field in enumerate(form_fields):
            if field.field_type == 9:
                date_pickers.append(i)
            if field.field_type == 10:
                datetime_pickers.append(i)
            if field.required and field.field_type in normal_fields:
                required_normal_fields.append(i)
            if field.required and field.field_type in choice_fields:
                required_choice_fields.append(i)

        # For Assign to Field
        if request.user.user_profiles.user_role == 'admin':
            print "yes it is admin who is logged in"
            org_obj = Organization.objects.get(super_admin=request.user.user_profiles.admin)
        elif request.user.user_profiles.user_role == 'super_admin':
            print "yes it is super admin who is logged in"
            org_obj = Organization.objects.get(super_admin__id=request.user.id)
        else:
            print "yes it is employee who is logged in"
            org_obj = Organization.objects.get(employees=request.user)

        frm_object = OrgForms.objects.get(id=int(pk))

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

        return render_to_response(self.template1, {'form_fields': form_fields, 'server_url': server_url,
                                                   'serial_no': new_serial_no, 'field_entries': field_entries,
                                                   'date_pickers': date_pickers, 'datetime_pickers': datetime_pickers,
                                                   'required_normal_fields': required_normal_fields,
                                                   'required_choice_fields': required_choice_fields,
                                                   'normal_fields': normal_fields, 'choice_fields': choice_fields,
                                                   'employees': employees},
                                  context_instance=RequestContext(request),)


    @method_decorator(custom_login_required)
    def post(self, request, pk=None, key=None, *args, **kwargs):

        org_form_obj = OrgForms.objects.get(id=int(pk))

        try:
            last_serial_no = FormEntries.objects.filter(org_form__id=int(pk)).latest('id').serial_no
            new_serial_no = last_serial_no + 1
        except:
            new_serial_no = 1

        if org_form_obj.allow_accept_reject == 'yes':
            entry_status = 'need_action'
        else:
            entry_status = ''

        form_entry_data = FormEntries(org_form=org_form_obj, org_member=request.user, serial_no=new_serial_no,
                                      entry_status=entry_status)
        if key:
            mapped_one = FormEntries.objects.get(id=int(key))
            form_entry_data.mapped_entry = mapped_one

        try:
            assign_to_id = request.POST['assign_to']
            form_entry_data.assigned_to = User.objects.get(id=int(assign_to_id))
            form_entry_data.assigned_by = request.user
        except:
            pass

        form_entry_data.save()

        form_fields = FormFields.objects.filter(org_form__id=int(pk))

        for i, field in enumerate(form_fields):
            field_val = 'field_value'+str(i)

            if field.field_type in [1, 2, 5, 7]:
                try:
                    field_posted_val = request.POST[field_val]
                except:
                    field_posted_val = ''
                FormFieldEntries(form_entry=form_entry_data, field_id=field, text_value=field_posted_val).save()

            if field.field_type == 3:
                try:
                    field_posted_val = request.POST[field_val]
                except:
                    field_posted_val = ''
                FormFieldEntries(form_entry=form_entry_data, field_id=field, email_value=field_posted_val).save()

            if field.field_type in [4, 6]:
                try:
                    field_posted_val = ','.join(request.POST.getlist(field_val))
                except:
                    field_posted_val = ''
                FormFieldEntries(form_entry=form_entry_data, field_id=field, choice_value=field_posted_val).save()

            if field.field_type == 8:
                try:
                    field_posted_val = request.FILES[field_val]
                except:
                    field_posted_val = ''
                FormFieldEntries(form_entry=form_entry_data, field_id=field, file_value=field_posted_val).save()

            if field.field_type == 11:
                try:
                    field_posted_val = request.POST[field_val]
                except:
                    field_posted_val = ''
                FormFieldEntries(form_entry=form_entry_data, field_id=field, url_value=field_posted_val).save()

            if field.field_type == 12:
                try:
                    field_posted_val = request.POST[field_val]
                except:
                    field_posted_val = ''
                FormFieldEntries(form_entry=form_entry_data, field_id=field, number_value=field_posted_val).save()

            if field.field_type == 9:
                try:
                    field_posted_val = datetime.datetime.strptime(str(request.POST[field_val]), "%b %d,%Y").date()
                except:
                    field_posted_val = ''
                FormFieldEntries(form_entry=form_entry_data, field_id=field, date_value=field_posted_val).save()

            if field.field_type == 10:
                try:
                    field_posted_val = datetime.datetime.strptime(str(request.POST[field_val]), "%b %d,%Y %I:%M %p")
                except:
                    field_posted_val = ''
                FormFieldEntries(form_entry=form_entry_data, field_id=field, datetime_value=field_posted_val).save()

        if key:
            return HttpResponseRedirect(reverse('view-form-entry', kwargs={'pk': key}))
        else:
            return HttpResponseRedirect(reverse('display-form-entries', kwargs={'pk': pk}))
