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
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics

from django.conf import settings
from apps.utils import utils
from models import *
import forms
import serializers

def ng_trade(request):
    return render(request, 'ng-trade.html')

class MerchantDetail(generics.RetrieveAPIView):
    queryset = Merchant.objects.all()
    serializer_class = serializers.MerchantSerializer

class CategoryList(APIView):

    def get(self, request, merchant_type=None):
        categories = Category.objects.filter(parent_category__isnull=True)

        if merchant_type == 'validated':
            serializer = serializers.CategoryValidatedSerializer(categories)
        elif merchant_type == 'candidates':
            serializer = serializers.CategoryCandidatesSerializer(categories)
        elif merchant_type == 'blocked':
            serializer = serializers.CategoryBlockedSerializer(categories)
        else:
            serializer = serializers.CategorySerializer(categories)
            
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

class ValidateMerchant(APIView):

    def get(self, request, pk):
        if not request.user.has_perm("trade.change_merchant"):
            return HttpResponseForbidden()
        mer = get_object_or_404(Merchant, pk=pk)
    
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
