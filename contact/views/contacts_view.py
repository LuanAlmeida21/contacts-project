from django.shortcuts import get_object_or_404, render

from contact.models import Contact

# Create your views here.


def index(request):
    contacts = Contact.objects.filter(show=True).order_by('-id')[10:20]
    context = {
        'contacts': contacts
    }

    return render(
        request,
        'contact/index.html',
        context
    )


def contact(request, contact_id):

    single_contact = get_object_or_404(Contact.objects.filter(pk=contact_id))

    context = {
        'contact': single_contact
    }

    return render(
        request,
        'contact/single_contact.html',
        context,
    )
