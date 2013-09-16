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
        if self.id:
            return hd_addresses.donationsCurrentSubKeyFast(self.id).bitcoin_address()
        return ''

    @property
    def freicoin_address_value(self):
        if self.freicoin_address:
            return self.freicoin_address.address.encode('base58')
        return ''

    @property
    def bitcoin_address_value(self):
        if self.bitcoin_address:
            return self.bitcoin_address.address.encode('base58')
        return ''

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
