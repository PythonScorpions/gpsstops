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
       print "pass", password
       user.is_active = False
       user.password = make_password(password)
       print "password:", user.password
       user.save()
       proform.user = user
       proform.save()
       return proform


class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()

    class Meta:
        model = UserProfiles
        exclude = ('user',)

    def __init__(self, *args, **kwargs):

        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['mobile'].widget.attrs['class'] = 'form-control'
        self.fields['skypeid'].widget.attrs['class'] = 'form-control'
        self.fields['country'].widget.attrs['class'] = 'form-control'

    def save(self,**kwargs):
       proform = super(ProfileUpdateForm, self).save(commit = False, **kwargs)
       user = User.objects.get(email=self.cleaned_data.get("email",False))
       user.first_name = self.cleaned_data.get("first_name",False)
       user.last_name = self.cleaned_data.get("last_name",False)
       user.username = self.cleaned_data.get("email",False)
       user.email = self.cleaned_data.get("email",False)
       password = self.cleaned_data.get("password",False)
       user.is_active = True
       user.save()
       proform.user = user
       proform.save()
       return proform

