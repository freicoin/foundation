from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect

from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context

from django.contrib.auth.decorators import login_required

from models import *
import forms

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

@login_required
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

               #  admin_mail_t = get_template('admin_mail.html')
               #  admin_mail = admin_mail_t.render(Context({'org': org}))
               #  send_mail(
               #      "New organization registration: %s" % org.name,
               #      admin_mail,
               #      cd.get('email', 'noreply@freicoin.org'),
               #      ['admin@freicoin.org'],
               #      )

               # org_mail_t = get_template('org_mail.html')
               #  org_mail = org_mail_t.render(Context({'org': org}))
               #  send_mail(
               #      "Thanks for registering your organization !",
               #      org_mail,
               #      'noreply@freicoin.org',
               #      [org.email],
               #      )

                return HttpResponseRedirect('/join_nonprofits/thanks/')
        else:
            form = forms.OrganizationForm()
    except:
        raise Http404()

    return render(request, 'new_organiation.html', {'form': form})

def thanks(request):
    return render(request, 'thanks.html')
