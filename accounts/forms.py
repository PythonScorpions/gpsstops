from django import forms
from django.contrib.auth.hashers import make_password
from accounts.models import *
from django.contrib.auth.models import User


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
  # password = forms.CharField(widget=forms.PasswordInput)
  # confirm_password = forms.CharField(widget=forms.PasswordInput)

  def __init__(self, user, *args, **kwargs):
    super(UsersCreateForm, self).__init__(*args, **kwargs)
    self.user = user
    if self.user.user_profiles.user_role == 'admin':
      self.fields['user_role'].choices = [(u'employee','Employee')]
    else:
      self.fields['user_role'].choices = [(u'','------'), (u'admin','Admin'), (u'employee','Employee')]

  class Meta:
    model = UserProfiles
    exclude = ('user', 'admin', 'token', 'admin_status')


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
