# from django.contrib import messages
from django.contrib import auth, messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from contact.forms import PasswordForm, RegisterUser, UserUpdate


def register(request):

    if request.method == 'POST':
        form = RegisterUser(request.POST)

        if form.is_valid():
            form.save()
            return redirect('contact:user_login')

        return render(
            request,
            'contact/create.html',
            context={'form': form}
        )

    context = {
        'form': RegisterUser(),
    }

    return render(request, 'contact/user_create.html', context)


@login_required(login_url='contact:user_login')
def user_update(request):
    form = UserUpdate(instance=request.user)

    if request.method != 'POST':
        return render(
            request,
            'contact/user_create.html',
            context={'form': form}
        )

    form = UserUpdate(data=request.POST, instance=request.user)

    if not form.is_valid():
        return render(
            request,
            'contact/user_create.html',
            context={'form': form}
        )

    form.save()
    messages.add_message(request, messages.SUCCESS,
                         'Successfully updated your profile!')
    return redirect('contact:user_update')


@login_required(login_url='contact:user_login')
def user_password(request):
    old_password = request.POST.get('old_password')
    password1 = request.POST.get('new_password1')

    user = User.objects.get(id=request.user.id)

    if request.method == 'POST':

        form = PasswordForm(request.user, data=request.POST)

        if user.check_password(old_password) is False:
            form.set_old_password_flag()

        if form.is_valid():
            user.set_password(password1)
            user.save()
            update_session_auth_hash(request, form.user)
            messages.add_message(request, messages.SUCCESS,
                                 'Successfully updated your password!')
            return redirect('contact:user_update')

        return render(request, 'contact/user_create.html',
                      {'form': PasswordForm(request.user,
                                            data=request.POST)})
    return render(request,
                  'contact/user_create.html',
                  {'form': PasswordForm(request.user)})


def user_login(request):
    form = AuthenticationForm(request)

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)

        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            messages.add_message(request, messages.SUCCESS, 'Success Login')
            return render(request, 'contact/login_user.html',
                          context={'form': form})

        messages.add_message(request, messages.ERROR, 'Invalid Login')

    return render(request, 'contact/login_user.html',
                  context={'form': form})


@login_required(login_url='contact:user_login')
def user_logout(request):
    auth.logout(request)
    messages.add_message(request, messages.SUCCESS, 'Success Logout')
    return redirect('contact:user_login')
