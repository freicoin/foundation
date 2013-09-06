import six

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django_patterns.db.models.mixins import PositionalOrderMixin

from .fields import BitcoinAddress

class Organization(models.Model):
    name = models.CharField(max_length=40)
    website = models.URLField()
    email = models.EmailField()
    short_description = models.CharField(max_length=350)
    long_description = models.CharField(max_length=1500)
    user = models.ForeignKey(User)

    @property
    def bitcoin_address(self):
        return self.payment_addresses.filter(type=PaymentAddress.BITCOIN).get_back()

    @property
    def freicoin_address(self):
        return self.payment_addresses.filter(type=PaymentAddress.FREICOIN).get_back()

    @property
    def foundation_address(self):
        return self.payment_addresses.filter(type=PaymentAddress.FOUNDATION).get_back()

    def __unicode__(self):
        return self.name

class PaymentAddress(PositionalOrderMixin):
    owner = models.ForeignKey(Organization, related_name='payment_addresses')
    address = BitcoinAddress(max_length=34)

    BITCOIN    = 'bitcoin'
    FREICOIN   = 'freicoin'
    FOUNDATION = 'foundation'
    TYPE_CHOICES = {
        BITCOIN:    _(u"Bitcoin"),
        FREICOIN:   _(u"Freicoin"),
        FOUNDATION: _(u"Foundation"),}
    REVERSE_TYPE = dict((value,key) for key,value in six.iteritems(TYPE_CHOICES))
    type = models.CharField(choices=six.iteritems(TYPE_CHOICES), max_length=10)

    def __unicode__(self):
        return repr(self.address)

    class Meta(object):
        order_with_respect_to = ('owner',)
