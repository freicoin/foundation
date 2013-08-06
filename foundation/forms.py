from django import forms

from bitcoin.address import BitcoinAddress
from bitcoin.errors import *

class FrcAddressField(forms.CharField):
    def validate(self, value):
        # Use the parent's handling of required fields, etc.
        super(FrcAddressField, self).validate(value)

        try:
            if len(value) > 0: 
                addr = BitcoinAddress(value.decode('base58'))
        except (InvalidAddressError, VersionedPayloadError, 
                HashChecksumError, InvalidBase58Error):
            raise forms.ValidationError("Not a valid address.")
