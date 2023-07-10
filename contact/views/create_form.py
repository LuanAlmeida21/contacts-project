from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from contact.forms import ContactForm
from contact.models import Contact


def create(request):
    title_create = 'Create'
    form_action = reverse('contact:create')

    if request.method == 'POST':

        form = ContactForm(request.POST)

        context = {
            'form': form,
            'form_action': form_action,
            'title': title_create
        }

        if form.is_valid():
            contact = form.save()
            return redirect('contact:update', contact_id=contact.id)

        return render(
            request,
            'contact/create.html',
            context
        )

    context = {
        'form': ContactForm(),
        'form_action': form_action,
        'title': title_create
    }

    return render(
        request,
        'contact/create.html',
        context
    )


def update(request, contact_id):

    title_update = 'Update'
    contact = get_object_or_404(Contact, id=contact_id, show=True)
    form_action = reverse('contact:update', args=(contact_id,))

    if request.method == 'POST':

        form = ContactForm(request.POST, instance=contact)

        context = {
            'form': form,
            'form_action': form_action,
            'title': title_update,
        }

        if form.is_valid():
            contact = form.save()
            return redirect('contact:update', contact_id=contact.id)

        return render(
            request,
            'contact/create.html',
            context
        )

    context = {
        'form': ContactForm(instance=contact),
        'form_action': form_action,
        'title': title_update,
    }

    return render(
        request,
        'contact/create.html',
        context
    )


def delete(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id, show=True)

    contact.delete()
    return redirect('contact:index')
