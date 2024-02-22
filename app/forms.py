from django import forms
from app.models import *

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email','password']
        widgets = {'password':forms.PasswordInput(attrs={
        'placeholder': 'Enter your password',
        'maxlength': '20',
        'autocomplete': 'off',
        'class': 'password-input',
        'data-toggle': 'password-strength-meter'
    })}
        help_texts = {'username':''}


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['address','profile_pic']
