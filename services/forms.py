from django import forms
from services.models import *
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError


class SerCategoryForm(forms.ModelForm):

    class Meta:
        model = ServiceCategory
        exclude = ('super_admin',)
        labels = {
            'cat_description': _('Description'),
        }


class SerSubCategoryForm(forms.ModelForm):

    class Meta:
        model = ServiceSubCategory
        exclude = ('super_admin',)
        labels = {
            'sub_cat_description': _('Description'),
        }


class ServiceForm(forms.ModelForm):

    class Meta:
        model = Services
        # exclude = ('super_admin',)
        # labels = {
        #     'sub_cat_description': _('Description'),
        # }

    def clean_end_price(self):
        start_price = self.cleaned_data.get("start_price", False)
        end_price = self.cleaned_data.get("end_price", False)
        print type(start_price)
        if not end_price > start_price:
            raise forms.ValidationError("End Price Should be greater than start price")
        return end_price
    # files = MultiFileField(min_num=1, max_num=3, max_file_size=1024*1024*5)
    #
    # def save(self, commit=True):
    #     instance = super(ProductForm, self).save(commit)
    #     for each in self.cleaned_data['files']:
    #         ProductImages.objects.create(product_image=each, product=instance)
    #
    #     return instance

# class MultiFileInput(forms.FileInput):
#     def render(self, name, value, attrs={}):
#         attrs['multiple'] = 'multiple'
#         return super(MultiFileInput, self).render(name, None, attrs=attrs)
#
#     def value_from_datadict(self, data, files, name):
#         if hasattr(files, 'getlist'):
#             return files.getlist(name)
#         else:
#             return [files.get(name)]
#
#
# class MultiFileField(forms.FileField):
#     widget = MultiFileInput
#     default_error_messages = {
#         'min_num': u"Ensure at least %(min_num)s files are uploaded (received %(num_files)s).",
#         'max_num': u"Ensure at most %(max_num)s files are uploaded (received %(num_files)s).",
#         'file_size': u"File: %(uploaded_file_name)s, exceeded maximum upload size."
#     }
#
#     def __init__(self, *args, **kwargs):
#         self.min_num = kwargs.pop('min_num', 0)
#         self.max_num = kwargs.pop('max_num', None)
#         self.maximum_file_size = kwargs.pop('maximum_file_size', None)
#         super(MultiFileField, self).__init__(*args, **kwargs)
#
#     def to_python(self, data):
#         ret = []
#         for item in data:
#             ret.append(super(MultiFileField, self).to_python(item))
#         return ret
#
#     def validate(self, data):
#         super(MultiFileField, self).validate(data)
#         num_files = len(data)
#         if len(data) and not data[0]:
#             num_files = 0
#         if num_files < self.min_num:
#             raise ValidationError(self.error_messages['min_num'] % {'min_num': self.min_num, 'num_files': num_files})
#             return
#         elif self.max_num and  num_files > self.max_num:
#             raise ValidationError(self.error_messages['max_num'] % {'max_num': self.max_num, 'num_files': num_files})
#         for uploaded_file in data:
#             if uploaded_file.size > self.maximum_file_size:
#                 raise ValidationError(self.error_messages['file_size'] % { 'uploaded_file_name': uploaded_file.name})
#
#
# class ImageForm(forms.Form):
#     files = MultiFileField(max_num = 10, min_num = 1, maximum_file_size = 1024*1024*5)