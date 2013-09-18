from django import forms

from djangular.forms.angular_model import NgModelFormMixin
from .models import *

class MerchantForm(NgModelFormMixin, forms.ModelForm):

    def __init__(self, *args, **kwargs):
        kwargs.update(scope_prefix='merchant')
        super(MerchantForm, self).__init__(*args, **kwargs)
        self.fields['short_description'].widget=forms.Textarea(
            attrs={'ng-model': 'merchant.short_description', 'cols': 50, 'rows': 5})
        self.fields['long_description'].widget=forms.Textarea(
            attrs={'ng-model': 'merchant.long_description', 'cols': 50, 'rows': 10})

    class Meta:
        model = Merchant
        fields = ['name', 'category', 'website', 
                  'short_description', 'long_description']
