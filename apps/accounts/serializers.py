from rest_framework import serializers

from django.contrib import auth
from django.contrib.auth.models import User

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate_username(self, attrs, source):
        if User.objects.filter(username__exact=attrs[source]).count() == 0:
            raise serializers.ValidationError("There's no user %s." % attrs[source])
        return attrs

    def validate(self, attrs):
        self.user = auth.authenticate(username=attrs['username'], password=attrs['password'])
        if self.user is None:
            msg = "Please enter a correct username and password. Note that both fields may be case-sensitive."            
            raise serializers.ValidationError(msg)
        elif not self.user.is_active:
            msg = "Disabled account. Did you receive the confirmation email? Check your spam folder."
            raise serializers.ValidationError(msg)

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()
    password2 = serializers.CharField()

    def validate_username(self, attrs, source):
        if User.objects.filter(username__exact=attrs[source]).count():
            raise serializers.ValidationError("A user with that username already exists.")
        return attrs

    def validate_email(self, attrs, source):
        if User.objects.filter(email__exact=attrs[source]).count():
            raise serializers.ValidationError("This email address is already in use. Please supply a different email address.")
        return attrs

    def validate_password(self, attrs, source):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("The two password fields didn't match.")
        return attrs

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, attrs, source):
        # Make sure that no email is sent to a user that actually has
        # a password marked as unusable
        try:
            user = User.objects.get(email=attrs[source])
        except User.DoesNotExist:
            raise serializers.ValidationError("There's no usable password for that email address.")
        if not user.has_usable_password():
            raise serializers.ValidationError("There's no usable password for that email address.")
        return attrs

class ChangePassSerializer(serializers.Serializer):
    password = serializers.CharField()
    new_password = serializers.CharField()
    new_password2 = serializers.CharField()

    def __init__(self, user, *args, **kwargs):
        try:
            self.user = User.objects.get(pk=user.id)
        except User.DoesNotExist:
            self.user = User()
        super(ChangePassSerializer, self).__init__(*args, **kwargs)

    def validate_password(self, attrs, source):
        if self.user.id and not self.user.check_password(attrs['password']):
            raise serializers.ValidationError("Your old password was entered incorrectly. "
                                              "Please enter it again.")
        return attrs

    def validate_new_password(self, attrs, source):
        if self.user.id and attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError("The two password fields didn't match.")
        return attrs

    def validate(self, attrs):
        if not self.user.id:
            raise serializers.ValidationError("You have to login to change your password.")            
        return attrs

    def save(self, commit=True):
        self.user.set_password(self.object['new_password'])
        if commit:
            self.user.save()
        return self.user
