from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from captcha.fields import ReCaptchaField

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    captcha = ReCaptchaField(attrs={'theme' : 'clean'}, label='')

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "captcha")

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
