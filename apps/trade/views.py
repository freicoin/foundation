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

from django.conf import settings
from apps.utils import utils
from models import *
import forms

def ng_trade(request):
    return render(request, 'ng-trade.html')

def serialize_category(category, merchant_type):
    if merchant_type == MerchantListView.VALIDATED:
        merchants = category.merchants.filter(validated_by__isnull=False)
    elif merchant_type == MerchantListView.CANDIDATES:
        merchants = category.merchants.filter(validated_by__isnull=True
                                              ).filter(validated__isnull=True)
    elif merchant_type == MerchantListView.BLOCKED:
        merchants = category.merchants.filter(validated_by__isnull=True
                                              ).filter(validated__isnull=False)

    mer_list = []
    for mer in merchants:
        mer = model_to_dict(mer, fields=['id', 'name', 'website', 'short_description'])
        mer_list.append(mer)
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


class MerchantListView(JSONResponseMixin, View):
    VALIDATED    = 'validated'
    CANDIDATES   = 'candidates'
    BLOCKED = 'blocked'
    def get_merchants(self):
        categories = Category.objects.filter(parent_category__isnull=True)
        return serialize_categories(categories, self.VALIDATED)
    def get_candidates(self):
        categories = Category.objects.filter(parent_category__isnull=True)
        return serialize_categories(categories, self.CANDIDATES)
    def get_blocked(self):
        categories = Category.objects.filter(parent_category__isnull=True)
        return serialize_categories(categories, self.BLOCKED)

class MerchantDetailView(JSONResponseMixin, View):
    def get_merchant(self, merchant_id=None):
        mer = Merchant.objects.get(pk=self.kwargs['mer_id'])
        return model_to_dict(mer, fields=[], exclude=[])

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
def mer_edit(request, id=None, template_name='new_organiation.html'):

    if id:
        mer = get_object_or_404(Merchant, pk=id)
        if (not request.user.has_perm("trade.change_merchant")
            and mer.user != request.user):
            return HttpResponseForbidden()
    else:
        mer = Merchant(user=request.user)

    form = forms.MerchantForm(request.POST or None, instance=mer)

    if form.is_valid():

        mer = form.save()
        mer.save()

        mer.email = request.user.email
        send_new_mer_mails(mer)

        msg = "Thank you for submitting your request. It will be validated by a human soon."
        return render(request, 'messages_list.html', {'messages': [msg]})

    return render(request, template_name, {'form': form})

@login_required
def mer_validate(request, id=None):
    if not request.user.has_perm("trade.change_merchant"):
        return HttpResponseForbidden()
    mer = get_object_or_404(Merchant, pk=id)
    
    if mer.validated_by:
        mer.validated_by = None
        mer.save()
        msg = "Merchant %s has been invalidated." % mer.name
    else:
        mer.validated_by = request.user
        if mer.validated:
            mer.save()
            msg = "Merchant %s is valid again." % mer.name
        else:
            mer.validated = datetime.now()
            mer.save()
            msg = "Merchant %s has been validated." % mer.name

    return render(request, 'messages_list.html', {'messages': [msg]})
