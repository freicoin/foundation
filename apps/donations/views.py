import json
from datetime import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponseForbidden

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

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
            serializer = serializers.CategorySerializer(categories, many=True)
            
        return Response(serializer.data)

class OrganizationDetail(generics.RetrieveAPIView):
    queryset = Organization.objects.all()
    serializer_class = serializers.OrganizationSerializer

def send_new_org_mails(org, email):
    context = {'org': org}

    utils.send_html_mail('mail/donations_mod_mail.html', context, 
                         "New organization registration: %s" % org.name, 
                         org.email, 'foundation@freicoin.org')

    utils.send_html_mail('mail/org_mail.html', context, 
                         "Thanks for registering your organization !", 
                         'foundation@freicoin.org', '%s, %s' % (org.email, email))

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

            serializer = serializers.OrganizationSerializer(org)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
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
            send_new_org_mails(org, request.user.email)

            serializer = serializers.OrganizationSerializer(org)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
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
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
