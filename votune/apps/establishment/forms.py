from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from votune.models import Account


class AccountEditForm(forms.ModelForm):
    email = forms.EmailField(required=True, label="Your email")
    first_name = forms.CharField(label="First name")
    last_name = forms.CharField(label="Last name")

    class Meta:
        model = User
        fields = ("first_name",
                  "last_name",
                  "email",)

    def __init__(self, *args, **kwargs):
        super(AccountEditForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class UserNameEditForm(forms.ModelForm):
    username = forms.CharField(max_length=30, min_length=4, label="New username")

    class Meta:
        model = User
        fields = ("username",)

    def clean_username(self):
        username = self.cleaned_data['username']
        print("checking username")

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already taken.")
        return username

    def __init__(self, *args, **kwargs):
        super(UserNameEditForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class OtherInfoEditForm(ModelForm):
    class Meta:
        model = Account
        fields = ("company",
                  "address", "postal_code", "phone",)

    def __init__(self, *args, **kwargs):
        super(OtherInfoEditForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class PasswordChangeForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label='Repeat password', max_length=30,
                                       min_length=4)
    password = forms.CharField(widget=forms.PasswordInput(), label='New password', max_length=30, min_length=4)

    class Meta:
        model = User
        fields = ('password',)
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean_confirm_password(self):
        password1 = self.cleaned_data['password']
        password2 = self.cleaned_data['confirm_password']

        if password1 != password2:
            raise forms.ValidationError("Passwords didn't match.")

    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

