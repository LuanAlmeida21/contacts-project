# flake8: noqa
from typing import Any, Dict

from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from contact.models import Contact

# from django.core.exceptions import ValidationError


class RegisterUser(UserCreationForm):

    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username',
                  'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            self.add_error('email',
                           ValidationError('Email already exists', code='Invalid'))

        return email

    def clean(self):
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')

        if first_name == last_name:
            msg = ValidationError(
                'Last name cannot be equal first name.', code='Invalid')
            self.add_error('last_name', msg)

        return super().clean()


class UserUpdate(forms.ModelForm):

    first_name = forms.CharField(min_length=3,
                                 max_length=30,
                                 required=True,
                                 error_messages={
                                     'min_length': f'Please, add more than 3 letters. '},
                                 )

    last_name = forms.CharField(min_length=3,
                                max_length=50,
                                required=True,
                                error_messages={
                                    'min_length': f'Please, add more than 3 letters. '},
                                )

    username = forms.CharField(disabled=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        current_email = self.instance.email

        if email != current_email:
            if User.objects.filter(email=email).exists():
                self.add_error('email',
                               ValidationError('Email already exists. ', code='Invalid'))
        return email


class ContactForm(forms.ModelForm):

    picture = forms.ImageField(required=False, widget=forms.FileInput(
        attrs={
            'accept': 'image/*',
        }
    )
    )

    class Meta:
        model = Contact
        fields = ('first_name', 'last_name', 'phone', 'email',
                  'description', 'category', 'picture')


class PasswordForm(PasswordChangeForm):

    old_password = forms.CharField(
        label='Current Password', required=False, widget=forms.PasswordInput)

    new_password1 = forms.CharField(
        label='New Password',
        required=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html
    )

    new_password2 = forms.CharField(
        label='Verify Password', required=False, widget=forms.PasswordInput)

    def clean_new_password1(self):
        new_password1 = self.cleaned_data.get('new_password1')
        if new_password1:
            try:
                if new_password1:
                    password_validation.validate_password(new_password1)
            except ValidationError as errors:
                self.add_error('new_password1', ValidationError(errors))
        return new_password1

    old_password_flag = True

    def set_old_password_flag(self):
        self.old_password_flag = False

        return 0

    def clean_old_password(self, *args, **kwargs):
        old_password = self.cleaned_data.get('old_password')

        if not old_password:
            raise forms.ValidationError("You must enter your old password.")

        if self.old_password_flag is False:
            raise forms.ValidationError(
                "The old password that you have entered is wrong.")

        return super().clean_old_password()

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')
