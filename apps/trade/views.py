import json
from datetime import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponseForbidden
from django.conf import settings

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics

from django.conf import settings
from apps.utils import utils
from models import *
import serializers

class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategoryShortSerializer

class CategoryTree(APIView):

    def get(self, request, merchant_type=None):
        categories = Category.objects.filter(parent_category__isnull=True)

        if merchant_type == 'validated':
            serializer = serializers.CategoryValidatedSerializer(categories)
        elif merchant_type == 'candidate':
            serializer = serializers.CategoryCandidatesSerializer(categories)
        elif merchant_type == 'blocked':
            serializer = serializers.CategoryBlockedSerializer(categories)
        else:
            serializer = serializers.CategorySerializer(categories)
            
        return Response(serializer.data)

class MerchantDetail(generics.RetrieveAPIView):
    queryset = Merchant.objects.all()
    serializer_class = serializers.MerchantSerializer

def send_new_mer_mails(mer, email):
    context = {'merchant': mer}

    admins = User.objects.filter(groups__name='trade_mod')
    if (admins.count() <= 0):
        admins = User.objects.filter(is_superuser=True)
    admin_mails = ""
    for user in admins:
        admin_mails += user.email + ', '
    # Remove the last ', '
    admin_mails = admin_mails[:-2]

    utils.send_html_mail('mail/trade_mod_mail.html', context, 
                         "New merchant registration: %s" % mer.name, 
                         email,
                         admin_mails)

    utils.send_html_mail('mail/merchant_mail.html', context, 
                         "Thanks for registering your business !", 
                         'noreply@freicoin.org', email)

class EditMerchant(APIView):

    def put(self, request, pk):

        mer = get_object_or_404(Merchant, pk=pk)
        if (not request.user.has_perm("trade.change_merchant")
            and mer.user != request.user):
            msg = "You don't have permissions to edit merchant %s." % pk
            return Response({"Error:": [msg]}, status=status.HTTP_403_FORBIDDEN)

        data = request.DATA
        data['user'] = mer.user.id
        serializer = serializers.MerchantSerializer(mer, data=data)
        if serializer.is_valid():
            
            mer = serializer.save()
            mer.save()

            serializer = serializers.MerchantSerializer(mer)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):

        data = request.DATA
        data['user'] = request.user.id
        serializer = serializers.MerchantSerializer(data=data)
        if serializer.is_valid():
            
            mer = serializer.save()
            mer.save()
            send_new_mer_mails(mer, request.user.email)

            serializer = serializers.MerchantSerializer(mer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ValidateMerchant(APIView):

    def put(self, request, pk):
        if ( not request.user.is_superuser and 
              request.user.groups.filter(name='trade_mod').count() == 0 ):
            msg = "You don't have permissions to validate merchants."
            return Response({"Error:": [msg]}, status=status.HTTP_403_FORBIDDEN)
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
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
