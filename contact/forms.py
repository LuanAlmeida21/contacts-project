# flake8: noqa
from django import forms
from django.contrib.auth.forms import UserCreationForm

from contact.models import Contact

# from django.core.exceptions import ValidationError


class RegisterUser(UserCreationForm):
    ...


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
