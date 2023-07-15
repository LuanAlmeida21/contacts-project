from django.contrib.auth.models import AnonymousUser
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from contact.models import Contact

# Create your views here.


def index(request):
    if request.user.is_anonymous:
        contacts = Contact.objects.filter(
            show=True, owner=AnonymousUser.id).order_by('-id')
    else:
        contacts = Contact.objects.filter(
            show=True, owner=request.user).order_by('-id')

    paginator = Paginator(contacts, 10)  # Show 10 contacts per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'site_title': 'Default - Contacts'
    }

    return render(
        request,
        'contact/index.html',
        context
    )


def contact(request, contact_id):

    if not request.user.is_anonymous:
        single_contact = get_object_or_404(
            Contact.objects.filter(pk=contact_id, owner=request.user))

        context = {
            'contact': single_contact,
        }

        return render(
            request,
            'contact/single_contact.html',
            context,
        )

    single_contact = get_object_or_404(
        Contact.objects.filter(pk=contact_id, owner=AnonymousUser.id))

    context = {
        'contact': single_contact,
    }

    return render(
        request,
        'contact/single_contact.html',
        context,
    )


def search(request):

    search_value = request.GET.get('q', '').strip()
    query = (Q(first_name__icontains=search_value) |
             Q(last_name__icontains=search_value) |
             Q(phone__icontains=search_value) |
             Q(email__icontains=search_value))

    if search_value == '':
        return redirect('contact:index')

    if request.user.is_anonymous:
        contacts = Contact.objects.filter(
            show=True, owner=AnonymousUser.id).filter(query).order_by('-id')
    else:
        contacts = Contact.objects.filter(
            show=True, owner=request.user).filter(query).order_by('-id')

    paginator = Paginator(contacts, 10)  # Show 10 contacts per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_value': search_value,
    }

    return render(request, 'contact/index.html', context)
