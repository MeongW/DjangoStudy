from django import forms
from .models import Account
from django.core.exceptions import ValidationError

class SignUpForm(forms.ModelForm):
    account_email = forms.EmailField(required=True)
    account_pw = forms.CharField(max_length=32, required=True, widget=forms.PasswordInput)
    account_name = forms.CharField(max_length=32, required=True)

    class Meta:
        model = Account
        fields = ['account_email', 'account_pw', 'account_name']

class LoginForm(forms.Form):
    account_email = forms.EmailField(required=True)
    account_pw = forms.CharField(max_length=32, required=True, widget=forms.PasswordInput)