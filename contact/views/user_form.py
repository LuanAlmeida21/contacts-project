from django.contrib import messages
from django.shortcuts import redirect, render

from contact.forms import RegisterUser


def register(request):

    form = RegisterUser(request.POST)
    context = {
        'form': form,
        'site_title': 'Register',
    }

    if request.method == 'POST':

        form = RegisterUser(request.POST)

        if form.is_valid():
            form.save()
            return redirect('contact:index')

    return render(request, 'contact/user_create.html', context)
