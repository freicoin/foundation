from django import forms
from captcha.fields import ReCaptchaField
from foundation.forms import FrcAddressField

class FaucetForm(forms.Form):
    frc_address = FrcAddressField(max_length=34, label='Freicoin address:')
    captcha = ReCaptchaField(attrs={'theme' : 'clean'}, label='')
