from django import forms
from .models import Fyers_Access_Token, Fyers_Auth_Inputs


class UserLoginForm(forms.Form):
    """UserLoginForm definition."""

    # TODO: Define form fields here

    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput())


class Fyers_Access_TokenForm(forms.ModelForm):
    """Form definition for ."""

    class Meta:
        """Meta definition for form."""

        model = Fyers_Access_Token
        fields = '__all__'
