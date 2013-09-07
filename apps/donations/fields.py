from django.utils.translation import ugettext_lazy as _

from django.db import models
from django.db.models import fields

import bitcoin.base58
from bitcoin.address import BitcoinAddress

class BitcoinAddressField(fields.CharField):
    __metaclass__ = models.SubfieldBase
    description = _(u"A bitcoin address, stored as a base58 character string.")

    def to_python(self, value):
        if value is None:
            return None
        if isinstance(value, BitcoinAddressField):
            return value
        return BitcoinAddressField(value.decode('base58'))

    def get_prep_value(self, value):
        if value is None:
            return None
        if not isinstance(value, BitcoinAddress):
            return value
        return value.encode('base58')

    def south_field_triple(self):
        "Returns a suitable description of this field for South."
        # We'll just introspect the _actual_ field.
        from south.modelsinspector import introspector
        field_class = '.'.join([self.__class__.__module__, self.__class__.__name__])
        args, kwargs = introspector(self)
        # That's our definition!
        return (field_class, args, kwargs)
