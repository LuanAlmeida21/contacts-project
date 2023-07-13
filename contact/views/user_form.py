# from django.contrib import messages
from django.contrib import auth, messages
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render

from contact.forms import RegisterUser


def register(request):

    if request.method == 'POST':
        form = RegisterUser(request.POST)

        if form.is_valid():
            form.save()
            return redirect('contact:index')

        return render(
            request,
            'contact/create.html',
            context={'form': form}
        )

    context = {
        'form': RegisterUser(),
        'site_title': 'Register',
    }

    return render(request, 'contact/user_create.html', context)


def user_login(request):
    form = AuthenticationForm(request)

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)

        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            messages.add_message(request, messages.SUCCESS, 'Success Login')
            return render(request, 'contact/login_user.html', {'form': form})

        messages.add_message(request, messages.ERROR, 'Invalid Login')

    return render(request, 'contact/login_user.html', context={'form': form})


def user_logout(request):
    auth.logout(request)
    return redirect('contact:login')
