import json

from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponseForbidden
from django.views.generic import View
from django.forms.models import model_to_dict

from django.contrib.auth.decorators import login_required

from djangular.views.mixins import JSONResponseMixin, HttpResponseBadRequest

from django.conf import settings
from apps.utils import utils
from models import *
import forms

def ng_donations(request):
    return render(request, 'ng-donations.html')

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
        org = Organization.objects.get(pk=self.kwargs['org_id'])
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
def org_edit(request, id=None, template_name='new_organiation.html'):

    if id:
        org = get_object_or_404(Organization, pk=id)
        if org.user != request.user:
            return HttpResponseForbidden()
    else:
        org = Organization(user=request.user)

    form = forms.OrganizationForm(request.POST or None, instance=org)

    if form.is_valid():

        org = form.save()
        org.save()

        send_new_org_mails(org)

        return redirect('org_thanks')

    return render(request, template_name, {'form': form})

def thanks(request):
    return render(request, 'thanks.html')
