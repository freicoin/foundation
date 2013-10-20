from django.core.context_processors import csrf
from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth.tokens import default_token_generator

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics

# TODO change from base36 to base64 on later django versions
from django.utils.http import int_to_base36, base36_to_int
# from django.utils.encoding import force_bytes
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

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
        serializer = serializers.LoginSerializer(data=request.DATA)
        if serializer.is_valid():
            auth.login(request, serializer.user)
            msg = "You have succesfuly logged in."
            return Response({msg}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordReset(APIView):

    def put(self, request):
        serializer = serializers.PasswordResetSerializer(data=request.DATA)
        if serializer.is_valid():
            email = serializer.object['email']
            user = User.objects.get(email=email)
            context = {
                'email': email,
                'uid': int_to_base36(user.id),
                # 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
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
        msg = "You have succesfuly logged out."
        return Response({msg}, status=status.HTTP_202_ACCEPTED)

class Register(APIView):

    def post(self, request):

        serializer = serializers.RegisterSerializer(data=request.DATA)
        if serializer.is_valid():
            try:
                user = User.objects.create_user(
                    serializer.object['username'],
                    serializer.object['email'],
                    serializer.object['password']
                    )
                user.is_active = False
                user.save()

                email = user.email
                context = {
                    'email': email,
                    'uid': int_to_base36(user.id),
                    'user': user,
                    'token': default_token_generator.make_token(user),
                    }
                utils.send_html_mail('confirmation_mail.html', context, 
                                     "Freicoin Foundation email confirmation", 
                                     'noreply@freicoin.org', email)

                msg = "You've registered as %s. You should receive a confirmation email shortly." % serializer.object['username']
                return Response({msg}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)

class ChangePass(APIView):

    def put(self, request):
        serializer = serializers.ChangePassSerializer(data=request.DATA, user=request.user)
        if serializer.is_valid():
            serializer.save()
            return Response({"You've succesfully changed your password."}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.template.response import TemplateResponse
from django.shortcuts import resolve_url

# Doesn't need csrf_protect since no-one can guess the URL
@sensitive_post_parameters()
@never_cache
def registration_confirm(request, uidb36=None, token=None,
                           template_name='registration_complete.html'):

    assert uidb36 is not None and token is not None # checked by URLconf
    try:
        uid = base36_to_int(uidb36)
        # uid = urlsafe_base64_decode(uidb64)
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        title = 'Email confirmation complete'
        message = 'The registration is complete. You may go ahead and log in now.'
    else:
        title = 'Email confirmation unsuccessful'
        message = "The email confirmation link was invalid, possibly because it has already been used. Please check that you haven't been validated already by trying to log in."

    login_url = resolve_url(settings.LOGIN_URL)
    context = {
        'title': title,
        'message': message,
        'login_url': login_url}
    return TemplateResponse(request, template_name, context)
