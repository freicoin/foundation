import json

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
from .fields import BitcoinAddressField
import forms

def ng_donations(request):
    return render(request, 'ng-donations.html', 
                  {'frc_explorer': settings.FRC_EXPLORER,
                   'btc_explorer': settings.BTC_EXPLORER})

def mapOrgToShortDict(org):
    org_dict = model_to_dict(org, fields=['id', 'name', 'website', 'short_description'])
    org_dict['foundation_address'] = org.foundation_address_value
    return org_dict

def mapOrgToDict(org):
    org_dict = model_to_dict(org, fields=['id', 'name', 'website', 'validated_by',
                                          'short_description', 'long_description'])
    org_dict['foundation_address'] = org.foundation_address_value
    org_dict['freicoin_address'] = org.freicoin_address_value
    return org_dict

def mapOrgListToDict(orgs):
    orgs_list = []
    for org in orgs:
        orgs_list.append(mapOrgToShortDict(org))
    return orgs_list

class OrgListView(JSONResponseMixin, View):
    def get_organizations(self):
        orgs = Organization.objects.filter(validated_by__isnull=False)
        return mapOrgListToDict(orgs)

    def get_candidates(self):
        orgs = Organization.objects.filter(
            validated_by__isnull=True).filter(foundation_address__isnull=True)
        return mapOrgListToDict(orgs)

    def get_blocked(self):
        orgs = Organization.objects.filter(
            validated_by__isnull=True).filter(foundation_address__isnull=False)
        return mapOrgListToDict(orgs)

class OrgDetailView(JSONResponseMixin, View):
    def get_organization(self, organization_id=None):
        org = Organization.objects.get(pk=self.kwargs['org_id'])
        return mapOrgToDict(org)

def send_new_org_mails(org):
    context = {'org': org}

    admins = User.objects.filter(groups__name='donations_admin')
    if (admins.count() <= 0):
        admins = User.objects.filter(is_superuser=True)
    admin_mails = ""
    for user in admins:
        admin_mails += user.email + ', '
    # Remove the last ', '
    admin_mails = admin_mails[:-2]

    utils.send_html_mail('mail/admin_mail.html', context, 
                         "New organization registration: %s" % org.name, 
                         org.email,
                         admin_mails)

    utils.send_html_mail('mail/org_mail.html', context, 
                         "Thanks for registering your organization !", 
                         'noreply@freicoin.org', org.email)

@login_required
def org_edit(request, id=None, template_name='new_organiation.html'):

    if id:
        org = get_object_or_404(Organization, pk=id)
        if (not request.user.has_perm("donations.change_organization")
            and org.user != request.user):
            return HttpResponseForbidden()
    else:
        org = Organization(user=request.user)

    form = forms.OrganizationForm(request.POST or None, instance=org,
                                  initial={'freicoin_address': org.freicoin_address_value,
                                           'bitcoin_address': org.bitcoin_address_value})

    if form.is_valid():

        org = form.save()
        org.save()

        cd = form.cleaned_data

        if cd['freicoin_address'] != org.freicoin_address_value:
            frc_addr = PaymentAddress()
            frc_addr.address = cd['freicoin_address']
            frc_addr.owner = org
            frc_addr.type = PaymentAddress.FREICOIN
            frc_addr.save()
            org.freicoin_address = frc_addr

        if cd['bitcoin_address'] != org.bitcoin_address_value:
            btc_addr = PaymentAddress()
            btc_addr.address = cd['bitcoin_address']
            btc_addr.owner = org
            btc_addr.type = PaymentAddress.BITCOIN
            btc_addr.save()
            org.bitcoin_address = btc_addr

        org.save()
        send_new_org_mails(org)

        msg = "Thank you for submitting your request. It will be validated by a human soon."
        return render(request, 'messages_list.html', {'messages': [msg]})

    return render(request, template_name, {'form': form})

def validate_org(org):
    available_addresses = AvailableAddress.objects.all()
    if available_addresses:
        sel_addr = available_addresses[0]
        ff_addr = PaymentAddress()
        ff_addr.address = sel_addr.address
        ff_addr.owner = org
        ff_addr.type = PaymentAddress.FOUNDATION
        ff_addr.save()
        sel_addr.delete()
        org.foundation_address = ff_addr
        org.save()
        return "Organization %s has been validated." % org.name
    else:
        return "Organization %s cannot be validated because there's no available foundation addresses." % org.name

@login_required
def org_validate(request, id=None):
    org = get_object_or_404(Organization, pk=id)
    
    if org.validated_by:
        org.validated_by = None
        org.save()
        msg = "Organization %s has been invalidated." % org.name
    else:
        org.validated_by = request.user
        if org.foundation_address:
            org.save()
            msg = "Organization %s is valid again." % org.name
        else:
            msg = validate_org(org)

    return render(request, 'messages_list.html', {'messages': [msg]})
