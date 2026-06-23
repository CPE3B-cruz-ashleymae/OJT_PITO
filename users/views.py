from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.forms import AuthenticationForm


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            # Handle 'Remember Me'
            if request.POST.get('remember_me'):
                request.session.set_expiry(1209600)  # 2 weeks
            else:
                request.session.set_expiry(0)
            # Redirect superuser to admin dashboard
            if user.is_superuser:
                return redirect('admin_dashboard')
            return redirect('blog-home')
        else:
            # ✅ Pass error directly to template, not via messages
            return render(request, 'users/login.html', {
                'form': form,
                'error': 'Invalid username or password.'
            })
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


def custom_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return redirect('blog-home')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'users/profile.html', {'u_form': u_form, 'p_form': p_form})
