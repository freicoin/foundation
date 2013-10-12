import json
from datetime import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponseForbidden
from django.views.generic import View
from django.forms.models import model_to_dict

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from djangular.views.mixins import JSONResponseMixin, HttpResponseBadRequest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics

from apps.utils import utils
from models import *
from .fields import BitcoinAddressField
import serializers

class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategoryShortSerializer

class CategoryTree(APIView):

    def get(self, request, organization_type=None):
        categories = Category.objects.filter(parent_category__isnull=True)

        if organization_type == 'validated':
            serializer = serializers.CategoryValidatedSerializer(categories, many=True)
        elif organization_type == 'candidate':
            serializer = serializers.CategoryCandidatesSerializer(categories, many=True)
        elif organization_type == 'blocked':
            serializer = serializers.CategoryBlockedSerializer(categories, many=True)
        else:
            serializer = serializers.CategorySerializer(categories)
            
        return Response(serializer.data)

class OrganizationDetail(generics.RetrieveAPIView):
    queryset = Organization.objects.all()
    serializer_class = serializers.OrganizationSerializer

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

class EditOrganization(APIView):

    def put(self, request, pk):

        org = get_object_or_404(Organization, pk=pk)
        if (not request.user.has_perm("donations.change_organization")
            and org.user != request.user):
            msg = "You don't have permissions to edit organization %s." % pk
            return Response({"Error:": [msg]}, status=status.HTTP_403_FORBIDDEN)

        data = request.DATA
        data['user'] = org.user.id
        serializer = serializers.OrganizationSerializer(org, data=data)
        if serializer.is_valid():
            
            org = serializer.save()
            org.save()

            if data['freicoin_address'] != org.freicoin_address_value:
                frc_addr = PaymentAddress()
                frc_addr.address = data['freicoin_address']
                frc_addr.owner = org
                frc_addr.type = PaymentAddress.FREICOIN
                frc_addr.save()
                org.freicoin_address = frc_addr

            if (data.has_key('bitcoin_address') 
                and data['bitcoin_address'] != org.bitcoin_address_value):

                btc_addr = PaymentAddress()
                btc_addr.address = data['bitcoin_address']
                btc_addr.owner = org
                btc_addr.type = PaymentAddress.BITCOIN
                btc_addr.save()
                org.bitcoin_address = btc_addr

            org.save()
            # org.email = request.user.email
            # send_new_org_mails(org)

            # return Response(serializer.data, status=status.HTTP_201_CREATED)
            msg = "Thank you for submitting your request. It will be validated by a human soon."
            return Response({"Success: ": [msg]}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):

        data = request.DATA
        data['user'] = request.user.id
        serializer = serializers.OrganizationSerializer(data=data)
        if serializer.is_valid():
            
            org = serializer.save()
            org.save()

            frc_addr = PaymentAddress()
            frc_addr.address = data['freicoin_address']
            frc_addr.owner = org
            frc_addr.type = PaymentAddress.FREICOIN
            frc_addr.save()
            org.freicoin_address = frc_addr

            if data.has_key('bitcoin_address'):
                btc_addr = PaymentAddress()
                btc_addr.address = data['bitcoin_address']
                btc_addr.owner = org
                btc_addr.type = PaymentAddress.BITCOIN
                btc_addr.save()
                org.bitcoin_address = btc_addr

            org.save()

            # org.email = request.user.email
            # send_new_org_mails(org)

            # return Response(serializer.data, status=status.HTTP_201_CREATED)
            msg = "Organization saved with id %s" % org.id
            return Response({"Success: ": [msg]}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ValidateOrganization(APIView):

    def put(self, request, pk):
        if ( not request.user.is_superuser and 
              request.user.groups.filter(name='donations_mod').count() == 0 ):
            msg = "You don't have permissions to validate organizations."
            return Response({"Error:": [msg]}, status=status.HTTP_403_FORBIDDEN)
        org = get_object_or_404(Organization, pk=pk)
    
        if org.validated_by:
            # Block organization
            org.validated_by = None
            org.save()
        else:
            org.validated_by = request.user
            if org.validated:
                # Unblock organization
                org.save()
            else:
                # Validate organization
                org.validated = datetime.now()
                org.save()

        serializer = serializers.OrganizationSerializer(org)
        return Response(serializer.data)
