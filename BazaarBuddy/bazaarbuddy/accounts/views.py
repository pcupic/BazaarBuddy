from django.shortcuts import render, get_object_or_404 ,redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .forms import RegistrationForm, UserEditForm
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.urls import reverse
from .models import UserProfile
from django.contrib.auth import logout as auth_logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['email']
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            user_type = form.cleaned_data['user_type']
            UserProfile.objects.create(user=user, user_type=user_type)

            return redirect('accounts:login')
    else:
        form = RegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                auth_login(request, user)
                return HttpResponseRedirect(reverse('core:homepage')) 
            else:
                messages.error(request, "Invalid email or password")
        else:
            messages.error(request, "Invalid email or password")
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})

@login_required
def profile(request):
    user_form = None 
    password_form = None  

    if request.method == 'POST':
        if 'edit_profile' in request.POST:
            user_form = UserEditForm(request.POST, instance=request.user)
            if user_form.is_valid():
                user = user_form.save(commit=False)
                user.username = user.email 
                user.save()
                messages.success(request, "Profile is updated.")
                return redirect('accounts:profile')  

        elif 'change_password' in request.POST:
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, password_form.user) 
                messages.success(request, "Your password has been changed.")
                return redirect('accounts:profile') 

        elif 'logout' in request.POST:
            auth_logout(request)
            messages.success(request, "You have successfully logged out.")
            return redirect('accounts:login')  

        elif 'delete_profile' in request.POST:
            user = request.user
            user.delete()
            auth_logout(request)  
            messages.success(request, "Your profile has been deleted.")
            return redirect('accounts:login') 

    else:
        user_form = UserEditForm(instance=request.user)
        password_form = PasswordChangeForm(request.user)

    return render(request, 'accounts/profile.html', {
        'user_form': user_form,
        'password_form': password_form,
    })
