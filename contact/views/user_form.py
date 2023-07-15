# from django.contrib import messages
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
# from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from contact.forms import RegisterUser, UserUpdate


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


@login_required(login_url='contact:user_login')
def user_update(request):
    form = UserUpdate(instance=request.user)

    if request.method != 'POST':
        return render(
            request,
            'contact/user_create.html',
            {'form': form}
        )

    form = UserUpdate(data=request.POST, instance=request.user)

    if not form.is_valid():
        return render(
            request,
            'contact/user_create.html',
            {'form': form}
        )

    form.save()
    messages.add_message(request, messages.SUCCESS, 'Success Update')
    return redirect('contact:user_update')


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


@login_required(login_url='contact:user_login')
def user_logout(request):
    auth.logout(request)
    return redirect('contact:user_login')
