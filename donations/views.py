from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.views.generic import TemplateView

from django.core.mail import send_mail

from donations.models import *
from donations import forms

home = TemplateView.as_view(template_name='index.html')
about = TemplateView.as_view(template_name='about.html')

def organization_list(request):
    organizations = Organization.objects.exclude(foundation_address__isnull=True).exclude(foundation_address__exact='')
    return render(request, 'organization_list.html', 
                  {'organization_list': organizations})

def organization_detail(request, organization_id=None):
    try:
        organization = Organization.objects.get(pk=organization_id)
    except Organization.DoesNotExist:
        raise Http404
    variables = {'org': organization}
    return render(request, 'organization_detail.html', variables)

def new_organization(request):
    try:
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
                org.save()

                # send_mail(
                #     "New organization registration: %s" % org.name,
                #     org.long_description,
                #     cd.get('email', 'noreply@freicoin.org'),
                #     ['admin@freicoin.org'],
                # )
                
                return HttpResponseRedirect('/join_nonprofits/thanks/')
        else:
            form = forms.OrganizationForm()
    except:
        raise Http404()

    return render(request, 'new_organiation.html', {'form': form})

def thanks(request):
    return render(request, 'thanks.html')
