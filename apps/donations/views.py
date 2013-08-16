from django.shortcuts import render, redirect
from django.http import Http404

from django.contrib.auth.decorators import login_required

from django.conf import settings
from apps.utils import utils

from models import *
import forms

def organization_list(request):
    organizations = Organization.objects.exclude(foundation_address__isnull=True
                                                 ).exclude(foundation_address__exact='')
    return render(request, 'organization_list.html', 
                  {'organization_list': organizations})

def organization_detail(request, organization_id=None):
    try:
        organization = Organization.objects.get(pk=organization_id)
    except Organization.DoesNotExist:
        raise Http404
    variables = {'org': organization}
    return render(request, 'organization_detail.html', variables)

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
