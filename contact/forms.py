# flake8: noqa
from django import forms
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
