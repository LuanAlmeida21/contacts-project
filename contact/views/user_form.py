# from django.contrib import messages
from django.contrib import auth, messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
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

    user = User.objects.get(username=request.user.username)
    old_password = request.POST.get('old_password')
    password = request.POST.get('password1')

    # print(old_password)
    # print(user.check_password(old_password))

    if user.check_password(old_password) and password:
        user.set_password(password)
        user.save()
        messages.add_message(request, messages.SUCCESS, 'Success Update')
        return redirect('contact:user_login')
    elif old_password and not form.verify_field():
        form.set_old_password()
        messages.add_message(request, messages.ERROR, 'Invalid Update')
        return redirect('contact:user_update')
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


def user_logout(request):
    auth.logout(request)
    return redirect('contact:user_login')
