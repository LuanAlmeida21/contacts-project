# flake8: noqa
from django import forms

from contact.models import Contact

# from django.core.exceptions import ValidationError


class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = ('first_name', 'last_name', 'phone', 'email', 'description', 'category')
