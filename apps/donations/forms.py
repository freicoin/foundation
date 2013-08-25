from django import forms

from apps.utils.forms import FrcAddressField

from .models import Organization

class OrganizationForm(forms.ModelForm):

    freicoin_address = FrcAddressField(max_length=34)
    bitcoin_address = FrcAddressField(required=False, max_length=34)

    def __init__(self, *args, **kwargs):
        super(OrganizationForm, self).__init__(*args, **kwargs)
        self.fields['short_description'].widget=forms.Textarea(attrs={'cols': 50, 'rows': 5})
        self.fields['long_description'].widget=forms.Textarea(attrs={'cols': 50, 'rows': 10})

    class Meta:
        model = Organization
        fields = ['name', 'website', 'email', 
                  'freicoin_address', 'bitcoin_address', 
                  'short_description', 'long_description']
