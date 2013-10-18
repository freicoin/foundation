from django.core.context_processors import csrf
from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.contrib import auth
from django.db import IntegrityError
from django.utils.http import int_to_base36
from django.contrib.auth.tokens import default_token_generator

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics

from django.conf import settings

from apps.utils import utils

import serializers

class CurrentUser(APIView):
    def get(self, request):
        user = request.user

        user_dict = {
            'id': user.id,
            'username': user.username,
            'autenticated': user.is_authenticated(),
            'admin': user.is_superuser,
            'groups': [g.name for g in user.groups.all()]}
        user_dict.update(csrf(request))

        return Response(user_dict, status=status.HTTP_200_OK)

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

class PasswordReset(APIView):

    def put(self, request):
        serializer = serializers.PasswordResetSerializer(data=request.DATA)
        if serializer.is_valid():
            email = serializer.object['email']
            user = auth.models.User.objects.get(email=email)
            context = {
                'email': email,
                'uid': int_to_base36(user.id),
                'user': user,
                'token': default_token_generator.make_token(user),
                }

            utils.send_html_mail('reset_password_mail.html', context, 
                             "Change password request", 
                             'noreply@freicoin.org', email)
            msg = "We've emailed you instructions for setting your password. You should be receiving them shortly. If you don't receive an email, please make sure you've entered the address you registered with, and check your spam folder."
            return Response({msg}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Logout(APIView):

    def post(self, request):
        auth.logout(request)
        msg = "You have logged out."
        return Response({"Success: ": [msg]}, status=status.HTTP_202_ACCEPTED)

class Register(APIView):

    def post(self, request):

        serializer = serializers.RegisterSerializer(data=request.DATA)
        if serializer.is_valid():
            try:
                auth.models.User.objects.create_user(
                    serializer.object['username'],
                    serializer.object['email'],
                    serializer.object['password']
                    )
                return Response({"You've registered as %s. Please, login." % 
                                 serializer.object['username']}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)

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

class ChangePass(APIView):

    def put(self, request):
        serializer = serializers.ChangePassSerializer(data=request.DATA, user=request.user)
        if serializer.is_valid():
            serializer.save()
            return Response({"You've succesfully changed your password."}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
