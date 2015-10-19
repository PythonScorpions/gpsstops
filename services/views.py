from django.shortcuts import render_to_response
from django.views.generic import View
from maps.views import custom_login_required
from django.utils.decorators import method_decorator
from django.template import RequestContext
import datetime
from gpsstops import settings
from services.forms import *
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from custom_forms.utils import *
import json


class SerCategory(View):
    template_name = 'services/service_category.html'

    @method_decorator(custom_login_required)
    def get(self, request, pk=None, key=None, *args, **kwargs):

        org_obj = retrieve_organization(request)

        categories = ServiceCategory.objects.filter(super_admin=org_obj)

        return render_to_response(self.template_name, {'categories': categories},
                                  context_instance=RequestContext(request),)


class SerSubCat(View):
    template_name = 'services/service_subcategory.html'

    @method_decorator(custom_login_required)
    def get(self, request, pk=None, key=None, *args, **kwargs):

        org_obj = retrieve_organization(request)

        subcategories = ServiceSubCategory.objects.filter(service_category__super_admin=org_obj)

        return render_to_response(self.template_name, {'subcategories': subcategories},
                                  context_instance=RequestContext(request),)


class SerList(View):
    template_name = 'services/service_list.html'

    @method_decorator(custom_login_required)
    def get(self, request, pk=None, key=None, *args, **kwargs):

        org_obj = retrieve_organization(request)

        services = Services.objects.filter(service_sub_category__service_category__super_admin=org_obj)

        return render_to_response(self.template_name, {'services': services},
                                  context_instance=RequestContext(request),)


class CategoryAdd(View):
    template_name = 'services/category_add.html'

    @method_decorator(custom_login_required)
    def get(self, request, pk=None, key=None, *args, **kwargs):

        if pk:
            cat_obj = ServiceCategory.objects.get(id=int(pk))
            initial_data = {
                'category_name': cat_obj.category_name,
                'cat_description': cat_obj.cat_description,
            }
            form = SerCategoryForm(instance=cat_obj, initial=initial_data)
        elif key:
            cat_obj = ServiceCategory.objects.get(id=int(key))
            cat_obj.delete()
            return HttpResponseRedirect(reverse('ser-category'))

        else:
            form = SerCategoryForm()

        return render_to_response(self.template_name, {'form': form},
                                  context_instance=RequestContext(request),)

    @method_decorator(custom_login_required)
    def post(self, request, pk=None, key=None, *args, **kwargs):

        org_obj = retrieve_organization(request)

        if pk:
            cat_obj = ServiceCategory.objects.get(id=int(pk))
            form = SerCategoryForm(data=request.POST, instance=cat_obj)
        else:
            form = SerCategoryForm(data=request.POST)

        if form.is_valid():
            if pk:
                cat_obj.category_name = form.cleaned_data['category_name']
                cat_obj.cat_description = form.cleaned_data['cat_description']
                cat_obj.save()
            else:
                new_category = ServiceCategory(category_name=form.cleaned_data['category_name'],
                                               cat_description=form.cleaned_data['cat_description'],
                                               super_admin=org_obj)
                new_category.save()
            return HttpResponseRedirect(reverse('ser-category'))
        else:
            print form.errors

        return render_to_response(self.template_name, {'form': form}, context_instance=RequestContext(request),)


class SubCategoryAdd(View):
    template_name = 'services/subcategory_add.html'

    @method_decorator(custom_login_required)
    def get(self, request, pk=None, key=None, *args, **kwargs):
        if pk:
            cat_obj = ServiceSubCategory.objects.get(id=int(pk))
            initial_data = {
                'subcategory_name': cat_obj.subcategory_name,
                'sub_cat_description': cat_obj.sub_cat_description,
                'service_category': cat_obj.service_category,
            }
            form = SerSubCategoryForm(instance=cat_obj, initial=initial_data)
        elif key:
            cat_obj = ServiceSubCategory.objects.get(id=int(key))
            cat_obj.delete()
            return HttpResponseRedirect(reverse('ser-subcat'))

        else:
            form = SerSubCategoryForm()

        return render_to_response(self.template_name, {'form': form},
                                  context_instance=RequestContext(request),)

    @method_decorator(custom_login_required)
    def post(self, request, pk=None, key=None, *args, **kwargs):

        if pk:
            cat_obj = ServiceSubCategory.objects.get(id=int(pk))
            form = SerSubCategoryForm(data=request.POST, instance=cat_obj)
        else:
            form = SerSubCategoryForm(data=request.POST)

        if form.is_valid():
            if pk:
                cat_obj.subcategory_name = form.cleaned_data['subcategory_name']
                cat_obj.sub_cat_description = form.cleaned_data['sub_cat_description']
                cat_obj.service_category = form.cleaned_data['service_category']
                cat_obj.save()
            else:
                new_category = ServiceSubCategory(subcategory_name=form.cleaned_data['subcategory_name'],
                                                  sub_cat_description=form.cleaned_data['sub_cat_description'],
                                                  service_category=form.cleaned_data['service_category'])
                new_category.save()
            return HttpResponseRedirect(reverse('ser-subcat'))
        else:
            print form.errors

        return render_to_response(self.template_name, {'form': form}, context_instance=RequestContext(request),)


class ServiceAdd(View):
    template_name = 'services/service_add.html'
    # form_class = ProfileUpdateForm

    @method_decorator(custom_login_required)
    def get(self, request, pk=None, key=None, *args, **kwargs):

        if pk:
            ser_obj = Services.objects.get(id=int(pk))
            initial_data = {
                'service_category': ser_obj.service_category,
                'service_sub_category': ser_obj.service_sub_category,
                'service_name': ser_obj.service_name,
                'service_desc1': ser_obj.service_desc1,
                'service_desc2': ser_obj.service_desc2,
                'about_service': ser_obj.about_service,
                'start_price': ser_obj.start_price,
                'end_price': ser_obj.end_price,
                'price_info': ser_obj.price_info,
                'service_image': ser_obj.service_image,
            }
            form = ServiceForm(instance=ser_obj, initial=initial_data)
            editing = "true"
            subcatid = ser_obj.service_sub_category.id

        elif key:
            ser_obj = Services.objects.get(id=int(key))
            ser_obj.delete()
            return HttpResponseRedirect(reverse('ser-list'))

        else:
            subcatid = 0
            editing = "false"
            form = ServiceForm()

        return render_to_response(self.template_name, {'form': form, 'editing': editing, 'subcatid': subcatid},
                                  context_instance=RequestContext(request),)

    @method_decorator(custom_login_required)
    def post(self, request, pk=None, key=None, *args, **kwargs):

        if pk:
            editing = 'true'
            ser_obj = Services.objects.get(id=int(pk))
            subcatid = ser_obj.service_sub_category.id
            form = ServiceForm(data=request.POST, files=request.FILES, instance=ser_obj)
        else:
            subcatid = 0
            editing = 'false'
            form = ServiceForm(data=request.POST, files=request.FILES)

        if form.is_valid():
            if pk:
                ser_obj.service_category = form.cleaned_data['service_category']
                ser_obj.service_sub_category = form.cleaned_data['service_sub_category']
                ser_obj.service_name = form.cleaned_data['service_name']
                ser_obj.service_desc1 = form.cleaned_data['service_desc1']
                ser_obj.service_desc2 = form.cleaned_data['service_desc2']
                ser_obj.about_service = form.cleaned_data['about_service']
                ser_obj.start_price = form.cleaned_data['start_price']
                ser_obj.end_price = form.cleaned_data['end_price']
                ser_obj.price_info = form.cleaned_data['price_info']
                ser_obj.service_image = form.cleaned_data['service_image']

                # if 'product_images' in request.FILES:
                #     for img in request.FILES.getlist('product_images'):
                #         ProductImages(product=pro_obj, product_image=img).save()
                # else:
                #     if not ProductImages.objects.filter(product=pro_obj):
                #         error_msg = True
                #         return render_to_response(self.template_name, {'form': form, 'error_msg': error_msg,
                #                                                        'editing': editing, 'product_id': product_id,
                #                                                        'subcatid': subcatid},
                #                                   context_instance=RequestContext(request),)
                ser_obj.save()
            else:
                # if 'product_images' not in request.FILES:
                #     error_msg = True
                #     return render_to_response(self.template_name, {'form': form, 'error_msg': error_msg,
                #                                                    'editing': editing, 'product_id': product_id,
                #                                                    'subcatid': subcatid},
                #                               context_instance=RequestContext(request),)
                # else:
                new_service = Services(service_category=form.cleaned_data['service_category'],
                                       service_sub_category=form.cleaned_data['service_sub_category'],
                                       service_name=form.cleaned_data['service_name'],
                                       service_desc1=form.cleaned_data['service_desc1'],
                                       service_desc2=form.cleaned_data['service_desc2'],
                                       about_service=form.cleaned_data['about_service'],
                                       start_price=form.cleaned_data['start_price'],
                                       end_price=form.cleaned_data['end_price'],
                                       price_info=form.cleaned_data['price_info'],
                                       service_image=form.cleaned_data['service_image'])
                new_service.save()

                    # for img in request.FILES.getlist('product_images'):
                    #     ProductImages(product=new_product, product_image=img).save()

            return HttpResponseRedirect(reverse('ser-list'))
        else:
            pass
            # if pk:
            #     if not ProductImages.objects.filter(product=pro_obj):
            #         error_msg = True
            #         return render_to_response(self.template_name, {'form': form, 'error_msg': error_msg,
            #                                                        'editing': editing, 'product_id': product_id,
            #                                                        'subcatid': subcatid},
            #                                   context_instance=RequestContext(request),)
            # else:
            #     if 'product_images' not in request.FILES:
            #         error_msg = True
            #     else:
            #         error_msg = False

        return render_to_response(self.template_name, {'form': form, 'editing': editing, 'subcatid': subcatid},
                                  context_instance=RequestContext(request),)


class SerInquiries(View):
    template_name = 'services/service_inquiries.html'

    @method_decorator(custom_login_required)
    def get(self, request, *args, **kwargs):

        org_obj = retrieve_organization(request)

        service_inquiries = ServiceInquiry.objects.filter(company_id__super_admin_id=org_obj).order_by('-id')

        return render_to_response(self.template_name, {'inquiries': service_inquiries},
                                  context_instance=RequestContext(request),)


class SerInquiriesView(View):
    template_name = 'services/service_inquiries_view.html'

    @method_decorator(custom_login_required)
    def get(self, request, pk=None, *args, **kwargs):

        service_inquiry = ServiceInquiry.objects.get(id=int(pk))

        return render_to_response(self.template_name, {'inquiry': service_inquiry},
                                  context_instance=RequestContext(request),)


class SerInquiryStatus(View):

    @method_decorator(custom_login_required)
    def get(self, request, pk=None, key=None, *args, **kwargs):

        service_inquiry = ServiceInquiry.objects.get(id=int(pk))

        if int(key) == 0:
            service_inquiry.accept_status = True
            service_inquiry.reject_status = False
        else:
            service_inquiry.accept_status = False
            service_inquiry.reject_status = True
        service_inquiry.save()

        return HttpResponseRedirect(reverse('ser-inquiry'))


class SerInquiryReply(View):
    template1 = 'services/service_inquiry_reply.html'
    template2 = 'services/service_inquiry_viewreply.html'

    @method_decorator(custom_login_required)
    def get(self, request, pk=None, *args, **kwargs):

        service_inquiry = ServiceInquiry.objects.get(id=int(pk))

        if ServiceInquiryReply.objects.filter(service_request_id=service_inquiry):
            print "replied"
            return render_to_response(self.template2, {'inquiry': service_inquiry},
                                      context_instance=RequestContext(request),)

        else:
            return render_to_response(self.template1, {'inquiry': service_inquiry},
                                      context_instance=RequestContext(request),)

    @method_decorator(custom_login_required)
    def post(self, request, pk=None, *args, **kwargs):

        service_inquiry = ServiceInquiry.objects.get(id=int(pk))

        inquiry_reply = ServiceInquiryReply(service_request_id=service_inquiry, comments=request.POST['reply'])
        inquiry_reply.save()

        return HttpResponseRedirect(reverse('ser-inquiry'))


def all_suboptions(request):
    # to retrieve categories in new campaign page
    cat_id = int(request.GET['cat_id'])
    sub_category_list = ServiceSubCategory.objects.filter(service_category__id=cat_id)
    category_dict = {}
    for cat in sub_category_list:
        category_dict[cat.id] = cat.subcategory_name
    return HttpResponse(json.dumps(category_dict), content_type="application/json")