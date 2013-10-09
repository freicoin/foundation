from rest_framework import serializers

from apps.utils.serializers import BtcAddressField
from .models import *

class OrganizationSerializer(serializers.ModelSerializer):
    category_name = serializers.Field(source='category.name')
    owner = serializers.Field(source='user.username')
    validated_by = serializers.Field(source='validated_by.username')
    validated = serializers.Field(source='validated')
    foundation_address = serializers.Field(source='foundation_address_value')
    freicoin_address = BtcAddressField(source='freicoin_address_value', max_length=34)
    bitcoin_address = BtcAddressField(source='bitcoin_address_value', required=False, max_length=34)

    class Meta:
        model = Organization
        fields = ('id', 'name', 'website', 'email', 'category', 'category_name', 'user', 'owner',
                  'short_description', 'long_description', 'validated', 'validated_by',
                  'foundation_address', 'freicoin_address', 'bitcoin_address')

class OrganizationShortSerializer(serializers.ModelSerializer):
    category_name = serializers.Field(source='category.name')
    user = serializers.Field(source='user.username')
    foundation_address = serializers.Field(source='foundation_address_value')

    class Meta:
        model = Organization
        fields = ('id', 'name', 'website', 'foundation_address', 'short_description')

class CategoryShortSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    organizations = OrganizationShortSerializer(source='organizations')
    inner_organizations = serializers.Field(source='inner_organizations')

    class Meta:
        model = Category
        fields = ('id', 'name', 'inner_organizations', 'organizations', 'child_categories')

CategorySerializer.base_fields['child_categories'] = CategorySerializer()

class CategoryValidatedSerializer(serializers.HyperlinkedModelSerializer):
    organizations = OrganizationShortSerializer(source='validated')
    inner_organizations = serializers.Field(source='inner_validated')

    class Meta:
        model = Category
        fields = ('id', 'name', 'inner_organizations', 'organizations', 'child_categories')

CategoryValidatedSerializer.base_fields['child_categories'] = CategoryValidatedSerializer()

class CategoryCandidatesSerializer(serializers.HyperlinkedModelSerializer):
    organizations = OrganizationShortSerializer(source='candidates')
    inner_organizations = serializers.Field(source='inner_candidates')

    class Meta:
        model = Category
        fields = ('id', 'name', 'inner_organizations', 'organizations', 'child_categories')

CategoryCandidatesSerializer.base_fields['child_categories'] = CategoryCandidatesSerializer()

class CategoryBlockedSerializer(serializers.HyperlinkedModelSerializer):
    organizations = OrganizationShortSerializer(source='blocked')
    inner_organizations = serializers.Field(source='inner_blocked')

    class Meta:
        model = Category
        fields = ('id', 'name', 'inner_organizations', 'organizations', 'child_categories')

CategoryBlockedSerializer.base_fields['child_categories'] = CategoryBlockedSerializer()
