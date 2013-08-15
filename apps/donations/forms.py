from django import forms
from apps.utils.forms import FrcAddressField

class OrganizationForm(forms.Form):
    name = forms.CharField(max_length=40)
    website = forms.URLField()
    email = forms.EmailField()
    freicoin_address = FrcAddressField(max_length=34)
    bitcoin_address = FrcAddressField(required=False, max_length=34)
    short_description = forms.CharField(widget=forms.Textarea, max_length=350)
    long_description = forms.CharField(widget=forms.Textarea, max_length=1500)
