from rest_framework import serializers

from django.contrib.auth.models import User

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()
    password2 = serializers.CharField()

    def validate_username(self, attrs, source):
        value = attrs[source]
        if User.objects.filter(username=value).count() > 0:
            raise serializers.ValidationError("The username already exists.")
        # if "django" not in value.lower():
        #     raise serializers.ValidationError("Blog post is not about Django")
        return attrs

    def validate_password(self, attrs, source):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("The passwords must match.")
        return attrs
