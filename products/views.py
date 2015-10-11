from django.shortcuts import render_to_response
from django.views.generic import View
from maps.views import custom_login_required
from django.utils.decorators import method_decorator
from django.template import RequestContext
import datetime
from gpsstops import settings
from products.forms import *
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from custom_forms.utils import *
import json


class ProCategory(View):
    template_name = 'products/product_category.html'
    # form_class = ProfileUpdateForm

    @method_decorator(custom_login_required)
    def get(self, request, pk=None, key=None, *args, **kwargs):

        org_obj = retrieve_organization(request)

        categories = ProductCategory.objects.filter(super_admin=org_obj)

        return render_to_response(self.template_name, {'categories': categories},
                                  context_instance=RequestContext(request),)


class ProSubCat(View):
    template_name = 'products/product_subcategory.html'
    # form_class = ProfileUpdateForm

    @method_decorator(custom_login_required)
    def get(self, request, pk=None, key=None, *args, **kwargs):

        org_obj = retrieve_organization(request)

        subcategories = ProductSubCategory.objects.filter(product_category__super_admin=org_obj)

        return render_to_response(self.template_name, {'subcategories': subcategories},
                                  context_instance=RequestContext(request),)


class ProList(View):
    template_name = 'products/product_list.html'
    # form_class = ProfileUpdateForm

    @method_decorator(custom_login_required)
    def get(self, request, pk=None, key=None, *args, **kwargs):

        org_obj = retrieve_organization(request)

        products = Products.objects.filter(product_sub_category__product_category__super_admin=org_obj)

        return render_to_response(self.template_name, {'products': products},
                                  context_instance=RequestContext(request),)


class CategoryAdd(View):
    template_name = 'products/category_add.html'

    @method_decorator(custom_login_required)
    def get(self, request, pk=None, key=None, *args, **kwargs):

        if pk:
            cat_obj = ProductCategory.objects.get(id=int(pk))
            initial_data = {
                'category_name': cat_obj.category_name,
                'cat_description': cat_obj.cat_description,
            }
            form = ProCategoryForm(instance=cat_obj, initial=initial_data)
        elif key:
            cat_obj = ProductCategory.objects.get(id=int(key))
            cat_obj.delete()
            return HttpResponseRedirect(reverse('pro-category'))

        else:
            form = ProCategoryForm()

        return render_to_response(self.template_name, {'form': form},
                                  context_instance=RequestContext(request),)

    @method_decorator(custom_login_required)
    def post(self, request, pk=None, key=None, *args, **kwargs):

        org_obj = retrieve_organization(request)

        if pk:
            cat_obj = ProductCategory.objects.get(id=int(pk))
            form = ProCategoryForm(data=request.POST, instance=cat_obj)
        else:
            form = ProCategoryForm(data=request.POST)

        if form.is_valid():
            if pk:
                cat_obj.category_name = form.cleaned_data['category_name']
                cat_obj.cat_description = form.cleaned_data['cat_description']
                cat_obj.save()
            else:
                new_category = ProductCategory(category_name=form.cleaned_data['category_name'],
                                               cat_description=form.cleaned_data['cat_description'],
                                               super_admin=org_obj)
                new_category.save()
            return HttpResponseRedirect(reverse('pro-category'))
        else:
            print form.errors

        return render_to_response(self.template_name, {'form': form}, context_instance=RequestContext(request),)


class SubCategoryAdd(View):
    template_name = 'products/subcategory_add.html'

    @method_decorator(custom_login_required)
    def get(self, request, pk=None, key=None, *args, **kwargs):
        if pk:
            cat_obj = ProductSubCategory.objects.get(id=int(pk))
            initial_data = {
                'subcategory_name': cat_obj.subcategory_name,
                'sub_cat_description': cat_obj.sub_cat_description,
                'product_category': cat_obj.product_category,
            }
            form = ProSubCategoryForm(instance=cat_obj, initial=initial_data)
        elif key:
            cat_obj = ProductSubCategory.objects.get(id=int(key))
            cat_obj.delete()
            return HttpResponseRedirect(reverse('pro-subcat'))

        else:
            form = ProSubCategoryForm()

        return render_to_response(self.template_name, {'form': form},
                                  context_instance=RequestContext(request),)

    @method_decorator(custom_login_required)
    def post(self, request, pk=None, key=None, *args, **kwargs):

        if pk:
            cat_obj = ProductSubCategory.objects.get(id=int(pk))
            form = ProSubCategoryForm(data=request.POST, instance=cat_obj)
        else:
            form = ProSubCategoryForm(data=request.POST)

        if form.is_valid():
            if pk:
                cat_obj.subcategory_name = form.cleaned_data['subcategory_name']
                cat_obj.sub_cat_description = form.cleaned_data['sub_cat_description']
                cat_obj.product_category = form.cleaned_data['product_category']
                cat_obj.save()
            else:
                new_category = ProductSubCategory(subcategory_name=form.cleaned_data['subcategory_name'],
                                                  sub_cat_description=form.cleaned_data['sub_cat_description'],
                                                  product_category=form.cleaned_data['product_category'])
                new_category.save()
            return HttpResponseRedirect(reverse('pro-subcat'))
        else:
            print form.errors

        return render_to_response(self.template_name, {'form': form}, context_instance=RequestContext(request),)


class ProductAdd(View):
    template_name = 'products/product_add.html'
    # form_class = ProfileUpdateForm

    @method_decorator(custom_login_required)
    def get(self, request, pk=None, key=None, *args, **kwargs):

        if pk:
            pro_obj = Products.objects.get(id=int(pk))
            initial_data = {
                'product_category': pro_obj.product_category,
                'product_sub_category': pro_obj.product_sub_category,
                'product_name': pro_obj.product_name,
                'product_desc1': pro_obj.product_desc1,
                'product_desc2': pro_obj.product_desc2,
                'about_product': pro_obj.about_product,
                'start_price': pro_obj.start_price,
                'end_price': pro_obj.end_price,
                'price_info': pro_obj.price_info,
                'features': pro_obj.features,
                'specs': pro_obj.specs,
            }
            form = ProductForm(instance=pro_obj, initial=initial_data)
            editing = "true"
            subcatid = pro_obj.product_sub_category.id

            product_images = ProductImages.objects.filter(product=pro_obj)
            product_id = int(pk)

        elif key:
            pro_obj = Products.objects.get(id=int(key))
            pro_obj.delete()
            return HttpResponseRedirect(reverse('pro-list'))

        else:
            subcatid = 0
            editing = "false"
            product_images = []
            form = ProductForm()
            product_id = 0

        return render_to_response(self.template_name, {'form': form, 'editing': editing, 'subcatid': subcatid,
                                                       'product_images': product_images, 'product_id': product_id},
                                  context_instance=RequestContext(request),)

    @method_decorator(custom_login_required)
    def post(self, request, pk=None, key=None, *args, **kwargs):

        if pk:
            editing = 'true'
            product_id = int(pk)
            pro_obj = Products.objects.get(id=int(pk))
            subcatid = pro_obj.product_sub_category.id
            form = ProductForm(data=request.POST, instance=pro_obj)
        else:
            subcatid = 0
            product_id = 0
            editing = 'false'
            form = ProductForm(data=request.POST)

        if form.is_valid():
            if pk:
                pro_obj.product_category = form.cleaned_data['product_category']
                pro_obj.product_sub_category = form.cleaned_data['product_sub_category']
                pro_obj.product_name = form.cleaned_data['product_name']
                pro_obj.product_desc1 = form.cleaned_data['product_desc1']
                pro_obj.product_desc2 = form.cleaned_data['product_desc2']
                pro_obj.about_product = form.cleaned_data['about_product']
                pro_obj.start_price = form.cleaned_data['start_price']
                pro_obj.end_price = form.cleaned_data['end_price']
                pro_obj.price_info = form.cleaned_data['price_info']
                pro_obj.features = form.cleaned_data['features']
                pro_obj.specs = form.cleaned_data['specs']

                if 'product_images' in request.FILES:
                    for img in request.FILES.getlist('product_images'):
                        ProductImages(product=pro_obj, product_image=img).save()
                else:
                    if not ProductImages.objects.filter(product=pro_obj):
                        error_msg = True
                        return render_to_response(self.template_name, {'form': form, 'error_msg': error_msg,
                                                                       'editing': editing, 'product_id': product_id,
                                                                       'subcatid': subcatid},
                                                  context_instance=RequestContext(request),)
                pro_obj.save()
            else:
                if 'product_images' not in request.FILES:
                    error_msg = True
                    return render_to_response(self.template_name, {'form': form, 'error_msg': error_msg,
                                                                   'editing': editing, 'product_id': product_id,
                                                                   'subcatid': subcatid},
                                              context_instance=RequestContext(request),)
                else:
                    new_product = Products(product_category=form.cleaned_data['product_category'],
                                           product_sub_category=form.cleaned_data['product_sub_category'],
                                           product_name=form.cleaned_data['product_name'],
                                           product_desc1=form.cleaned_data['product_desc1'],
                                           product_desc2=form.cleaned_data['product_desc2'],
                                           about_product=form.cleaned_data['about_product'],
                                           start_price=form.cleaned_data['start_price'],
                                           end_price=form.cleaned_data['end_price'],
                                           price_info=form.cleaned_data['price_info'],
                                           features=form.cleaned_data['features'],
                                           specs=form.cleaned_data['specs'])
                    new_product.save()

                    for img in request.FILES.getlist('product_images'):
                        ProductImages(product=new_product, product_image=img).save()

            return HttpResponseRedirect(reverse('pro-list'))
        else:
            if pk:
                if not ProductImages.objects.filter(product=pro_obj):
                    error_msg = True
                    return render_to_response(self.template_name, {'form': form, 'error_msg': error_msg,
                                                                   'editing': editing, 'product_id': product_id,
                                                                   'subcatid': subcatid},
                                              context_instance=RequestContext(request),)
            else:
                if 'product_images' not in request.FILES:
                    error_msg = True
                else:
                    error_msg = False

        return render_to_response(self.template_name, {'form': form, 'error_msg': error_msg, 'editing': editing,
                                                       'product_id': product_id, 'subcatid': subcatid},
                                  context_instance=RequestContext(request),)


def all_suboptions(request):
    # to retrieve categories in new campaign page
    cat_id = int(request.GET['cat_id'])
    sub_category_list = ProductSubCategory.objects.filter(product_category__id=cat_id)
    category_dict = {}
    for cat in sub_category_list:
        category_dict[cat.id] = cat.subcategory_name
    return HttpResponse(json.dumps(category_dict), content_type="application/json")


def delete_image(request):
    # to retrieve categories in new campaign page
    img_src = request.GET['img_src']
    product_id = int(request.GET['product_id'])

    for pro in ProductImages.objects.filter(product__id=product_id):
        if str(pro.product_image).split('/')[-1] == img_src:
            pro.delete()
            break
    return HttpResponse('success')