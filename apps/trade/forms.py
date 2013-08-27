from django import forms

from .models import *

class MerchantForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(MerchantForm, self).__init__(*args, **kwargs)
        self.fields['short_description'].widget=forms.Textarea(attrs={'cols': 50, 'rows': 5})
        self.fields['long_description'].widget=forms.Textarea(attrs={'cols': 50, 'rows': 10})

    class Meta:
        model = Merchant
        fields = ['name', 'category', 'website', 
                  'short_description', 'long_description']
