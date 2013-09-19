import json
from datetime import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponseForbidden
from django.views.generic import View
from django.forms.models import model_to_dict
from django.conf import settings

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from djangular.views.mixins import JSONResponseMixin, HttpResponseBadRequest
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.conf import settings
from apps.utils import utils
from models import *
import forms
import serializers

def ng_trade(request):
    return render(request, 'ng-trade.html')

def serialize_merchant_short(mer):
    return model_to_dict(mer, fields=['id', 'name', 'website', 'short_description'])

def serialize_merchant(mer):
    return model_to_dict(mer, fields=[], exclude=[])

def get_merchants(category, merchant_type):
    if merchant_type == JsonApiView.VALIDATED:
        merchants = category.merchants.filter(validated_by__isnull=False)
    elif merchant_type == JsonApiView.CANDIDATES:
        merchants = category.merchants.filter(validated_by__isnull=True
                                              ).filter(validated__isnull=True)
    elif merchant_type == JsonApiView.BLOCKED:
        merchants = category.merchants.filter(validated_by__isnull=True
                                              ).filter(validated__isnull=False)
    else:
        merchants = []
    mer_list = []
    for mer in merchants:
        mer_list.append( serialize_merchant_short(mer) )
    return mer_list 

def serialize_category(category, merchant_type):
    mer_list = get_merchants(category, merchant_type)
    mer_count = len(mer_list)

    categories = category.child_categories.all()
    cat_list = []
    for cat in categories:
        cat_dict = serialize_category(cat, merchant_type)
        if cat_dict['inner_merchants'] > 0:
            mer_count += cat_dict['inner_merchants']
            cat_list.append(cat_dict)

    return {'id': category.pk,
            'name': category.name,
            'merchants': mer_list,
            'inner_merchants': mer_count,            
            'child_categories': cat_list}

def serialize_categories(categories, merchant_type):
    cat_list = []
    for cat in categories:
        cat_dict = serialize_category(cat, merchant_type)
        if cat_dict['inner_merchants'] > 0:
            cat_list.append(cat_dict)
    return cat_list


class JsonApiView(JSONResponseMixin, View):
    VALIDATED    = 'validated'
    CANDIDATES   = 'candidates'
    BLOCKED = 'blocked'
    def get_categories(self):
        merchant_type = self.kwargs['merchant_type']
        if not merchant_type:
            merchant_type = self.VALIDATED
        categories = Category.objects.filter(parent_category__isnull=True)
        return serialize_categories(categories, merchant_type)

@api_view(['GET'])
def getMerchant(request, mer_id):
    mer = get_object_or_404(Merchant, pk=mer_id)
    serializer = serializers.MerchantSerializer(mer)
    return Response(serializer.data)

def send_new_mer_mails(mer):
    context = {'merchant': mer}

    admins = User.objects.filter(groups__name='trade_admin')
    if (admins.count() <= 0):
        admins = User.objects.filter(is_superuser=True)
    admin_mails = ""
    for user in admins:
        admin_mails += user.email + ', '
    # Remove the last ', '
    admin_mails = admin_mails[:-2]

    utils.send_html_mail('mail/admin_mail.html', context, 
                         "New merchant registration: %s" % mer.name, 
                         mer.email,
                         admin_mails)

    utils.send_html_mail('mail/merchant_mail.html', context, 
                         "Thanks for registering your business !", 
                         'noreply@freicoin.org', mer.email)

@login_required
def mer_edit(request, id=None, template_name='edit_merchant.html'):

    if id:
        mer = get_object_or_404(Merchant, pk=id)
        if (not request.user.has_perm("trade.change_merchant")
            and mer.user != request.user):
            return HttpResponseForbidden()
    else:
        mer = Merchant(user=request.user)

    form = forms.MerchantForm(request.POST or None, instance=mer)

    if (request.POST or id) and form.is_valid():

        mer = form.save()
        mer.save()

        mer.email = request.user.email
        send_new_mer_mails(mer)
        msg = "Thank you for submitting your request. It will be validated by a human soon."
        return render(request, template_name, {'msg': msg})

    return render(request, template_name, {'form': form})

@api_view(['GET', 'POST'])
def mer_validate(request, id):
    if not request.user.has_perm("trade.change_merchant"):
        return HttpResponseForbidden()
    mer = get_object_or_404(Merchant, pk=id)
    
    if mer.validated_by:
        # Block merchant
        mer.validated_by = None
        mer.save()
    else:
        mer.validated_by = request.user
        if mer.validated:
            # Unblock merchant
            mer.save()
        else:
            # Validate merchant
            mer.validated = datetime.now()
            mer.save()

    serializer = serializers.MerchantSerializer(mer)
    return Response(serializer.data)
