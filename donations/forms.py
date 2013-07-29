from django import forms

class OrganizationForm(forms.Form):
    name = forms.CharField(max_length=30)
    website = forms.URLField()
    short_description = forms.CharField(max_length=60)
    long_description = forms.CharField(widget=forms.Textarea, max_length=600)
    freicoin_address = forms.CharField(max_length=34)
    bitcoin_address = forms.CharField(required=False, max_length=34)
    email = forms.EmailField()
