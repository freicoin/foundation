from django.shortcuts import render
from django.http import Http404

def organization_list(request):
    raise Http404()

def new_organization(request):
    return render(request, 'new_organiation.html')
