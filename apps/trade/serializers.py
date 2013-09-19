from rest_framework import serializers

from .models import *

class MerchantSerializer(serializers.ModelSerializer):

    category_name = serializers.Field(source='category.name')

    class Meta:
        model = Merchant
        fields = ('id', 'name', 'website', 'category', 'category_name',
                  'short_description', 'long_description', 'validated', 'validated_by')
