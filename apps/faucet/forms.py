from django import forms
from captcha.fields import ReCaptchaField

class FaucetForm(forms.Form):
    frc_address = forms.CharField(max_length=34)
    captcha = ReCaptchaField(attrs={'theme' : 'clean'})
