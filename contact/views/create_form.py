# flake8: noqa
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from contact.forms import ContactForm
from contact.models import Contact


@login_required(login_url='contact:user_login')
def create(request):
    form_action = reverse('contact:create')

    if request.method == 'POST':

        form = ContactForm(request.POST, request.FILES)

        context = {
            'form': form,
            'form_action': form_action,
        }

        if form.is_valid():
            contact = form.save(commit=False)
            contact.owner = request.user
            contact.save()
            messages.add_message(request, messages.SUCCESS, 'Successfully Created')
            return redirect('contact:update', contact_id=contact.id)

        return render(
            request,
            'contact/create.html',
            context
        )

    context = {
        'form': ContactForm(),
        'form_action': form_action,
    }

    return render(
        request,
        'contact/create.html',
        context
    )


@login_required(login_url='contact:user_login')
def update(request, contact_id):

    contact = get_object_or_404(Contact, id=contact_id, show=True, owner=request.user)
    form_action = reverse('contact:update', args=(contact_id,))

    if request.method == 'POST':

        form = ContactForm(request.POST, request.FILES, instance=contact)

        context = {
            'form': form,
            'form_action': form_action,
        }

        if form.is_valid():
            contact = form.save()
            messages.add_message(request, messages.SUCCESS, 'Successfully Updated')
            return redirect('contact:contact', contact_id=contact.id)

        return render(
            request,
            'contact/create.html',
            context
        )

    context = {
        'form': ContactForm(instance=contact),
        'form_action': form_action,
    }

    return render(
        request,
        'contact/create.html',
        context
    )


@login_required(login_url='contact:user_login')
def delete(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id, show=True, owner=request.user)

    confirmation = request.POST.get('confirmation', 'no')
    context = {
        'contact': contact,
        'confirmation': confirmation
    }

    if confirmation == 'yes':
        contact.delete()
        messages.add_message(request, messages.SUCCESS, 'Successfully Deleted')
        return redirect('contact:index')

    return render(request, 'contact/single_contact.html', context=context)
