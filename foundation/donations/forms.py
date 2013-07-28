from django import forms

class OrganizationForm(forms.Form):
    name = forms.CharField(max_length=30)
    website = models.URLField()
    short_description = models.CharField(max_length=60)
    long_description = models.CharField(widget=forms.Textarea, max_length=600)
    freicoin_address = models.CharField(max_length=34)
    bitcoin_address = models.CharField(required=False, max_length=34)
    email = models.EmailField()
