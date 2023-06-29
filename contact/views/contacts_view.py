from django.shortcuts import get_object_or_404, render

from contact.models import Contact

# Create your views here.


def index(request):
    contacts = Contact.objects.filter(show=True).order_by('-id')[10:20]
    context = {
        'contacts': contacts,
        'site_title': 'Default'
    }

    return render(
        request,
        'contact/index.html',
        context
    )


def contact(request, contact_id):

    single_contact = get_object_or_404(Contact.objects.filter(pk=contact_id))

    site_title = f'{single_contact.first_name} {single_contact.last_name}'

    context = {
        'contact': single_contact,
        'site_title': site_title
    }

    return render(
        request,
        'contact/single_contact.html',
        context,
    )
