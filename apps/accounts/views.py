from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.contrib import auth
from django.db import IntegrityError

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics

# from apps.utils import captcha

from django.conf import settings

import serializers

class Login(APIView):

    def post(self, request):
        data = request.DATA
        user = auth.authenticate(username=data['username'], password=data['password'])
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                msg = "You are logged in."
                return Response({"Success: ": [msg]}, status=status.HTTP_202_ACCEPTED)
            else:
                msg = "Disabled account."
        else:
            msg = "Please enter a correct username and password. Note that both fields may be case-sensitive."
        return Response({"Error: ": [msg]}, status=status.HTTP_400_BAD_REQUEST)

class Logout(APIView):

    def post(self, request):
        auth.logout(request)
        msg = "You have logged out."
        return Response({"Success: ": [msg]}, status=status.HTTP_202_ACCEPTED)

class Register(APIView):

    def post(self, request):

        serialized = serializers.RegisterSerializer(data=request.DATA['register'])
        if serialized.is_valid():
            try:
                auth.models.User.objects.create_user(
                    serialized.init_data['username'],
                    serialized.init_data['email'],
                    serialized.init_data['password']
                    )
                return Response(serialized.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)

      # You need to implement your server side validation here.
      # Send the model.captcha object to the server and use some of the server side APIs to validate it
      # See https://developers.google.com/recaptcha/docs/


        # data = request.DATA['register']
        # recaptcha = request.DATA['recaptcha']
        # challenge = recaptcha['challenge']
        # response = recaptcha['response']
        # client = "85.53.142.15" #request.META['REMOTE_ADDR']
        # check_captcha = captcha.submit(challenge, response,  
        #                                settings.RECAPTCHA_PRIVATE_KEY, client)  
        # if check_captcha.is_valid:
        #     msg = "Valid captcha."
        #     return Response({"Success: ": [msg]}, status=status.HTTP_202_ACCEPTED)
        # else:
        #     msg = "Invalid captcha."
        #     return Response({"Error: ": [msg]}, status=status.HTTP_400_BAD_REQUEST)
