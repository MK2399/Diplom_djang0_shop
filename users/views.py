from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.template.context_processors import csrf
from .forms import LoginForm, UserRegistrForm, UserEditForm, ProfileEditForm
from .models import UserProfile


def user_login(request):
    if request.method == 'POST':
        args = {}
        args.update(csrf(request))
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username = cd['username']
            user = authenticate(username=cd['username'], password=cd['password'])
            request.session['username'] = username
            if user is not None:
                if user:
                    login(request, user)
                    return redirect('/')
                else:
                    args['login_error'] = 'Аккаунт удален'
                    return render(request, 'templates_users/login.html', args)
            else:
                args['login_error'] = 'Пользователь не найден'
                return render(request, 'templates_users/login.html', args)
    else:
        form = LoginForm()
    return render(request, 'templates_users/login.html', {'from': form})


def logouts(request):
    auth.logout(request)
    return redirect('/')


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            profile = UserProfile.objects.create(user=new_user)
            login(request, new_user)
            return redirect('/')
    else:
        user_form = UserRegistrForm()
    return render(request, 'templates_users/register.html', {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.userprofile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return render(request, 'templates_users/personal_data.html')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.userprofile)
    return render(request, 'templates_users/edit_profile.html', {'user_form': user_form,
                                                                'profile_form': profile_form})


def personal_data(request):
    return render(request, 'templates_users/personal_data.html')

