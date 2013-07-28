from django.shortcuts import render
from django.http import Http404

from donations.models import *

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
    return render(request, 'new_organiation.html')
