from rest_framework import serializers

from bitcoin.address import BitcoinAddress
from bitcoin.errors import *

class BtcAddressField(serializers.CharField):
    def validate(self, value):
        # Use the parent's handling of required fields, etc.
        super(BtcAddressField, self).validate(value)

        try:
            if len(value) > 0: 
                addr = BitcoinAddress(value.decode('base58'))
        except (InvalidAddressError, VersionedPayloadError, 
                HashChecksumError, InvalidBase58Error):
            raise serializers.ValidationError("Enter a valid address.")
