import json

from django.shortcuts import render, redirect
from django.http import Http404
from django.views.generic import View
from django.forms.models import model_to_dict

from django.contrib.auth.decorators import login_required

from djangular.views.mixins import JSONResponseMixin, HttpResponseBadRequest

from django.conf import settings
from apps.utils import utils
from models import *
import forms

def ng_view(request):
    return render(request, 'ng-template.html')

class OrgListView(JSONResponseMixin, View):
    def get_organizations(self):
        orgs = Organization.objects.exclude(foundation_address__isnull=True
                                            ).exclude(foundation_address__exact='')
        orgs_list = []
        for org in orgs:
            orgs_list.append(model_to_dict(org, fields=[], exclude=[]))
        return orgs_list

class OrgDetailView(JSONResponseMixin, View):
    # def get(self, request, *args, **kwargs):
    #     kwargs.update(action='get_organization')
    #     return super(OrgDetailView, self).get(self, request, *args, **kwargs)
    def get_organization(self, organization_id=None):
        org = Organization.objects.get(pk=self.kwargs['organization_id'])
        return model_to_dict(org, fields=[], exclude=[])

def send_new_org_mails(org):
    context = {'org': org}
    utils.send_html_mail('admin_mail.html', context, 
                         "New organization registration: %s" % org.name, 
                         org.email,
                         settings.DONATION_ADMIN_MAILS)

    utils.send_html_mail('org_mail.html', context, 
                         "Thanks for registering your organization !", 
                         'noreply@freicoin.org', org.email)

@login_required
def new_organization(request):

    if request.method == 'POST':
        form = forms.OrganizationForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data

            org = Organization()

            org.name = cd['name']
            org.website = cd['website']
            org.short_description = cd['short_description']
            org.long_description = cd['long_description']
            org.freicoin_address = cd['freicoin_address']
            org.bitcoin_address = cd['bitcoin_address']
            org.email = cd['email']
            org.user = request.user
            org.save()

            send_new_org_mails(org)

            return redirect('org_thanks')
    else:
        form = forms.OrganizationForm()

    return render(request, 'new_organiation.html', {'form': form})

def thanks(request):
    return render(request, 'thanks.html')

def organization_list(request):
    return render(request, 'organization_list.html')
