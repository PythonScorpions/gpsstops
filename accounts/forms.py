from django import forms
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

from accounts.models import *
from accounts.utils import *


class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    password1 = forms.CharField(label=("Password"), widget=forms.PasswordInput)
    password2 = forms.CharField(label=("Confirm Password"), widget=forms.PasswordInput)

    class Meta:
        model = UserProfiles
        exclude = ('user',)

    def __init__(self, *args, **kwargs):

        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs = {'class': 'input-search', 'placeholder': 'Name*'}
        self.fields['password1'].widget.attrs = {'class': 'input-search', 'placeholder': 'Password*'}
        self.fields['password2'].widget.attrs = {'class': 'input-search', 'placeholder': 'Confirm Password*'}
        self.fields['email'].widget.attrs = {'class': 'input-search', 'placeholder': 'Email*'}
        self.fields['address'].widget.attrs = {'class': 'input-search', 'placeholder': 'Address*'}
        self.fields['city'].widget.attrs = {'class': 'input-search', 'placeholder': 'City*'}
        self.fields['state'].widget.attrs = {'class': 'input-search', 'placeholder': 'State*'}
        self.fields['zip_code'].widget.attrs = {'class': 'input-search', 'placeholder': 'Zip code*'}
        self.fields['country'].widget.attrs = {'class': 'input-search', 'placeholder': 'Country*'}
        self.fields['phone_number'].widget.attrs = {'class': 'input-search', 'placeholder': 'Phone Number*'}
        self.fields['occupation'].widget.attrs = {'class': 'input-search', 'placeholder': 'Occupation*'}
        self.fields['company_name'].widget.attrs = {'class': 'input-search', 'placeholder': 'Company Name*'}


    def clean_email(self):
        email = self.cleaned_data.get("email",False)
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("User with this email already exists please try another.")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1",False)
        password2 = self.cleaned_data.get("password2",False)
        if not password1 == password2:
            raise forms.ValidationError("Two Password Field Should be Same")
        return password2

    def save(self, **kwargs):
       proform = super(RegisterForm, self).save(commit=False, **kwargs)
       user = User()
       user.first_name = self.cleaned_data.get("first_name", False)
       user.last_name = self.cleaned_data.get("last_name", False)
       user.username = self.cleaned_data.get("email", False)
       user.email = self.cleaned_data.get("email", False)
       password = self.cleaned_data.get("password2", False)
       user.is_active = False
       user.password = make_password(password)
       user.save()

       proform.user = user
       proform.admin_status = 'enable'
       proform.admin = user
       proform.user_role = 'super_admin'
       proform.save()
       return proform


class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150)
    email = forms.EmailField()

    class Meta:
        model = UserProfiles
        exclude = ('user',)

    def __init__(self, *args, **kwargs):

        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs = {'class': 'input-search', 'placeholder': 'Name*'}
        self.fields['email'].widget.attrs = {'class': 'input-search', 'placeholder': 'Email*'}
        self.fields['address'].widget.attrs = {'class': 'input-search', 'placeholder': 'Address*'}
        self.fields['city'].widget.attrs = {'class': 'input-search', 'placeholder': 'City*'}
        self.fields['state'].widget.attrs = {'class': 'input-search', 'placeholder': 'State*'}
        self.fields['zip_code'].widget.attrs = {'class': 'input-search', 'placeholder': 'Zip code*'}
        self.fields['country'].widget.attrs = {'class': 'input-search', 'placeholder': 'Country*'}
        self.fields['phone_number'].widget.attrs = {'class': 'input-search', 'placeholder': 'Phone Number*'}
        self.fields['occupation'].widget.attrs = {'class': 'input-search', 'placeholder': 'Occupation*'}
        self.fields['company_name'].widget.attrs = {'class': 'input-search', 'placeholder': 'Company Name*'}


    def save(self,**kwargs):
       proform = super(ProfileUpdateForm, self).save(commit=False, **kwargs)
       user = User.objects.get(email=self.cleaned_data.get("email", False))
       user.first_name = self.cleaned_data.get("first_name", False)
       user.last_name = self.cleaned_data.get("last_name", False)
       user.username = self.cleaned_data.get("email", False)
       user.email = self.cleaned_data.get("email", False)
       user.is_active = True
       user.save()
       proform.user = user
       proform.save()
       return proform


class UsersCreateForm(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    is_active = forms.BooleanField(required=False)

    def __init__(self, user, *args, **kwargs):

        super(UsersCreateForm, self).__init__(*args, **kwargs)
        self.user = user
        if self.user.is_authenticated() and self.user.user_profiles.user_role == 'admin':
          self.fields['user_role'].choices = [(u'employee','Employee')]
        else:
          self.fields['user_role'].choices = [(u'','------'), (u'admin','Admin'), (u'employee','Employee')]

    def clean_email(self):
        email = self.cleaned_data.get("email", False)
        try:
            u = self.instance.user
        except:
            u = None

        if User.objects.filter(email=email).exists() and not u:
            raise forms.ValidationError("Email already exists.")
        return email

    class Meta:
        model = UserProfiles
        exclude = ('user', 'admin', 'token', 'admin_status', 'occupation',
                    'company_name', 'is_active')


class UsersCreateSuperAdminForm(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    is_active = forms.BooleanField(required=False)

    def __init__(self, user, *args, **kwargs):
        super(UsersCreateSuperAdminForm, self).__init__(*args, **kwargs)

        self.user = user
        if self.user.is_authenticated() and self.user.user_profiles.user_role == 'admin':
          self.fields['user_role'].choices = [(u'employee','Employee')]
        else:
          self.fields['user_role'].choices = [(u'','------'), (u'admin','Admin'), (u'employee','Employee')]

        users_choices = [(self.user.id, 'Self')]
        for u in get_users(self.user).filter(user_profiles__user_role='admin'):
            users_choices.append((u.id, '%s %s' % (u.first_name, u.last_name)))
        self.fields['admin'].choices = users_choices

    def clean_email(self):
        email = self.cleaned_data.get("email", False)
        try:
            u = self.instance.user
        except:
            u = None

        if User.objects.filter(email=email).exists() and not u:
            raise forms.ValidationError("Email already exists.")
        return email

    class Meta:
        model = UserProfiles
        exclude = ('user', 'token', 'admin_status', 'occupation',
                    'company_name', 'is_active')


class UsersLoginForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        if any(self.errors):
          return

        if not self.cleaned_data['password'] == self.cleaned_data['confirm_password']:
          raise forms.ValidationError('Password didn\'t match')
        return self.cleaned_data


class RouteAssignmentForm(forms.Form):
    user = forms.IntegerField(widget=forms.widgets.Select())
    is_editable = forms.BooleanField(initial=True, required=False)

    def __init__(self, user, *args, **kwargs):
        super(RouteAssignmentForm, self).__init__(*args, **kwargs)

        users_choices = [(user.id, 'Self')]
        for u in User.objects.filter(user_profiles__admin=user).exclude(pk=user.id).distinct():
            users_choices.append((u.id, '%s %s' % (u.first_name, u.last_name)))
        self.fields['user'].widget.choices = users_choices

    def clean_user(self):
      try:
        user = User.objects.get(pk=self.cleaned_data['user'])
      except:
        raise forms.ValidationError("Invalid user.")
      else:
        return user


class CategoryForm(forms.ModelForm):

    class Meta:
        model = CategoryForForm
        exclude = ('status', 'created_at', 'updated_at', 'organization', 'serial_no')

    # def save(self, request, **kwargs):
    #     proform = super(CategoryForm, self).save(commit=False)
    #     try:
    #         last_serial_no = CategoryForForm.objects.last().serial_no
    #         new_serial_no = last_serial_no + 1
    #     except:
    #         new_serial_no = 1
    #     if request.user.user_profiles.user_role == 'admin':
    #         org_obj = Organization.objects.get(super_admin=request.user.user_profiles.admin)
    #     else:
    #         org_obj = Organization.objects.get(super_admin__id=request.user.id)
    #     new_category = CategoryForForm(category_name=self.cleaned_data['category_name'],
    #                                    remarks=self.cleaned_data['remarks'],
    #                                    organization=org_obj, status='active', serial_no=new_serial_no)
    #     new_category.save()
    #     return proform


class FormForOrgForm(forms.ModelForm):
    form_cat = forms.ChoiceField(label='Form Category')
    mapped_form = forms.ChoiceField(label='Map with other form')

    def __init__(self, user, *args, **kwargs):
        super(FormForOrgForm, self).__init__(*args, **kwargs)

        if user.user_profiles.user_role == 'admin':
            org_obj = Organization.objects.get(super_admin=user.user_profiles.admin)
        else:
            org_obj = Organization.objects.get(super_admin__id=user.id)
        cat_choices = []
        for cat in CategoryForForm.objects.filter(organization=org_obj):
            cat_choices.append((cat.id, cat.category_name))
        self.fields['form_cat'].widget.choices = cat_choices
        map_form_choices = [(0, 'None')]
        for form_obj in OrgForms.objects.filter(form_cat__organization=org_obj):
            map_form_choices.append((form_obj.id, form_obj.form_name))
        self.fields['mapped_form'].widget.choices = map_form_choices

    class Meta:
        model = OrgForms
        exclude = ('serial_no', 'status', 'created_at', 'updated_at', 'input_assign_to', 'display_assign_to',
                   'allow_accept_reject', 'input_assign_allow', 'display_assign_allow')


class WebThemeForm(forms.ModelForm):
    class Meta:
        model = WebTheme


class MobileThemeForm(forms.ModelForm):
    class Meta:
        model = Theme
