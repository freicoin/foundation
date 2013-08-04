from django import forms
from django.core.validators import validate_email
from bitcoin.address import BitcoinAddress

class FrcAddressField(forms.CharField):
    def validate(self, value):
        # Use the parent's handling of required fields, etc.
        super(FrcAddressField, self).validate(value)

        # TODO make a real address validation
        try:
            addr = BitcoinAddress(value.decode('base58'))
        except:
        # possible exceptions:
        # InvalidAddressError, VersionedPayloadError,
        # HashChecksumError, InvalidBase58Error
            raise forms.ValidationError("Not a valid address.")
