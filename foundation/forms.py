from django import forms
from django.core.validators import validate_email

class FrcAddressField(forms.CharField):
    def validate(self, value):
        # Use the parent's handling of required fields, etc.
        super(FrcAddressField, self).validate(value)

        # TODO make a real address validation
        if len(value) > 0 and not value.startswith('1'):
            raise forms.ValidationError("Not a valid address.")
