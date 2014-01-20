import six

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from .fields import BitcoinAddressField
from apps.donations import hd_addresses

class Category(models.Model):
    name = models.CharField(max_length=40)
    parent_category = models.ForeignKey('self', blank=True, null=True, 
                                        related_name="child_categories")

    @property
    def validated(self):
        return self.organizations.filter(validated_by__isnull=False)

    @property
    def candidates(self):
        return self.organizations.filter(validated_by__isnull=True
                                     ).filter(validated__isnull=True)
    @property
    def blocked(self):
        return self.organizations.filter(validated_by__isnull=True
                                     ).filter(validated__isnull=False)

    @property
    def inner_organizations(self):
        total = self.organizations.count()
        for cat in self.child_categories.all():
            total += cat.inner_organizations
        return total

    @property
    def inner_validated(self):
        total = self.validated.count()
        for cat in self.child_categories.all():
            total += cat.inner_validated
        return total

    @property
    def inner_candidates(self):
        total = self.candidates.count()
        for cat in self.child_categories.all():
            total += cat.inner_candidates
        return total

    @property
    def inner_blocked(self):
        total = self.blocked.count()
        for cat in self.child_categories.all():
            total += cat.inner_blocked
        return total

    def __unicode__(self):
        return self.name

class Organization(models.Model):
    name = models.CharField(max_length=40)

    category = models.ForeignKey('Category', related_name='organizations')
    website = models.URLField()
    email = models.EmailField()
    short_description = models.CharField(max_length=350)
    long_description = models.TextField()
    freicoin_address = models.ForeignKey('PaymentAddress', null=True, 
                                         related_name='freicoin_address_for')
    bitcoin_address = models.ForeignKey('PaymentAddress', null=True, 
                                        related_name='bitcoin_address_for')

    created = models.DateTimeField(auto_now_add=True)
    validated = models.DateTimeField(null=True)
    validated_by = models.ForeignKey(User, null=True, related_name="organizations_validated")
    user = models.ForeignKey(User)

    @property
    def foundation_address_value(self):
        if self.validated and self.id:
            return hd_addresses.donationsOrgAddress(self.id)
        return ''

    @property
    def freicoin_address_value(self):
        if self.freicoin_address:
            return self.freicoin_address.address.encode('base58')
        return ''

    @freicoin_address_value.setter
    def freicoin_address_value(self, value):
        pass

    @property
    def bitcoin_address_value(self):
        if self.bitcoin_address:
            return self.bitcoin_address.address.encode('base58')
        return ''

    @bitcoin_address_value.setter
    def bitcoin_address_value(self, value):
        pass

    @property
    def validation_state(self):
        if self.validated_by:
            return 'validated'
        elif self.validated:
            return 'blocked'
        else:
            return 'candidate'

    def __unicode__(self):
        return self.name

class PaymentAddress(models.Model):
    owner = models.ForeignKey(Organization, related_name='payment_addresses')
    address = BitcoinAddressField(max_length=34)
    timestamp = models.DateTimeField(auto_now_add=True)

    BITCOIN    = 'bitcoin'
    FREICOIN   = 'freicoin'
    TYPE_CHOICES = {
        BITCOIN:    _(u"Bitcoin"),
        FREICOIN:   _(u"Freicoin"),}
    REVERSE_TYPE = dict((value,key) for key,value in six.iteritems(TYPE_CHOICES))
    type = models.CharField(choices=six.iteritems(TYPE_CHOICES), max_length=10)

    def __unicode__(self):
        return repr(self.address)
