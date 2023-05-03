from django import forms

from django.core.exceptions import ValidationError


class CreateUser(forms.Form):
    name = forms.CharField(max_length=50, min_length=3)
    user_email = forms.CharField(max_length=100)
    password = forms.CharField(max_length=50, min_length=4)
