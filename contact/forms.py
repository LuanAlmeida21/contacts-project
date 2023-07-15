# flake8: noqa
from typing import Any, Dict

from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
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
                                 help_text='Required.')

    last_name = forms.CharField(min_length=3,
                                max_length=50,
                                required=True,
                                help_text='Required.')

    username = forms.CharField(disabled=True)

    old_password = forms.CharField(label='Old Password',
                                   strip=False,
                                   required=False,
                                   widget=forms.PasswordInput(
                                       attrs=(
                                           {"autocomplete": "current-password"})
                                   ))

    password1 = forms.CharField(label='New Password',
                                strip=False,
                                required=False,
                                widget=forms.PasswordInput(
                                    attrs=({'auto_complete': 'new_password'})),
                                help_text=password_validation.password_validators_help_text_html)

    password2 = forms.CharField(label='Confirm Password',
                                strip=False,
                                required=False,
                                widget=forms.PasswordInput(
                                    attrs=({'auto_complete': 'new_password'})),
                                )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')

    # def save(self, commit=True):
    #     cleaned_data = self.cleaned_data
    #     user = super().save(commit=False)
    #     password = cleaned_data.get('password1')

    #     if password:
    #         user.set_password(password)

    #     if commit:
    #         user.save()

    #     return user

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 or password2:
            if password1 != password2:
                self.add_error(
                    'password2',
                    ValidationError('Dont match passwords.')
                )

        return super().clean()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        current_email = self.instance.email

        if email != current_email:
            if User.objects.filter(email=email).exists():
                self.add_error('email',
                               ValidationError('Email already exists. ', code='Invalid'))
        return email

    old_password_flag = True

    def set_old_password(self):
        self.old_password_flag = False
        return 0

    verify = True

    def verify_field(self):
        self.verify = False
        return 0

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not old_password and self.verify == False:
            self.add_error('old_password', ValidationError(
                "You must enter your old password."))

        if self.old_password_flag == False:
            self.add_error('old_password', ValidationError(
                "The old password that you have entered is wrong."))

        return old_password

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if password1:
            try:
                if password1:
                    password_validation.validate_password(password1)
            except ValidationError as errors:
                self.add_error('password1', ValidationError(errors))
        return password1


class ContactForm(forms.ModelForm):

    picture = forms.ImageField(widget=forms.FileInput(
        attrs={
            'accept': 'image/*',
        }
    )
    )

    class Meta:
        model = Contact
        fields = ('first_name', 'last_name', 'phone', 'email',
                  'description', 'category', 'picture')
