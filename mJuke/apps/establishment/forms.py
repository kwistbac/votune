from django import forms
from django.contrib.auth.models import User
from mJuke.models import Account
from django.contrib.auth.forms import UserCreationForm


class AccountEditForm(forms.ModelForm):
    email = forms.EmailField(required=True, label="Your email")
    first_name = forms.CharField(label="First name")
    last_name = forms.CharField(label="Last name")

    class Meta:
        model = User
        fields = ("first_name",
                  "last_name",
                  "email",)


class UserNameEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username",)


class OtherInfoEditForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ("company",
                  "address", "postal_code", "phone",)


class PasswordChangeForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ( 'password',)
        widgets = {
            'password': forms.PasswordInput(),
        }