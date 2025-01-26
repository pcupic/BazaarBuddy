from django.shortcuts import render, get_object_or_404 ,redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.urls import reverse
from .models import UserProfile
from django.contrib.auth import logout as auth_logout
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
            
            try:
                user = User.objects.get(email=email)
                user = authenticate(request, username=user.username, password=password)
                
                if user is not None:
                    auth_login(request, user)
                    return HttpResponseRedirect(reverse('core:homepage')) 
                else:
                    messages.error(request, "Invalid email or password")
            except User.DoesNotExist:
                messages.error(request, "Invalid email or password")
        else:
            messages.error(request, "Invalid email or password")
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})

def admin_dashboard(request):
    if request.method == 'POST':  
        user_id = request.POST.get('user_id') 
        user = get_object_or_404(User, id=user_id)  
        if not user.is_superuser:  
            user.delete()
            messages.success(request, f"User '{user.username}' has been deleted.")
        else:
            messages.error(request, "You cannot delete an admin.")
        return redirect('accounts:admin_dashboard')

    users = User.objects.filter(profile__user_type__in=['moderator', 'regular'])
    return render(request, 'accounts/admin_dashboard.html', {'users': users})

from .forms import UserEditForm, PasswordChangeCustomForm

@login_required
def profile(request):
    if request.method == 'POST':
        if 'edit_profile' in request.POST:
            user_form = UserEditForm(request.POST, instance=request.user)
            if user_form.is_valid():
                user_form.save()  
                messages.success(request, "Profile is updated.")
                return redirect('accounts:profile')  
        elif 'logout' in request.POST:
            auth_logout(request)
            messages.success(request, "You have successfully logged out.")
            return redirect('accounts:login')  
        elif 'delete_profile' in request.POST:
            user = request.user
            user.delete()  
            auth_logout(request)  
            messages.success(request, "Your profile is deleted.")
            return redirect('accounts:login')  
        elif 'change_password' in request.POST:
            password_form = PasswordChangeCustomForm(request.user, request.POST)
            if password_form.is_valid():
                password_form.save() 
                messages.success(request, "Your password is changed.")
                return redirect('accounts:profile')  
        else:
            user_form = UserEditForm(instance=request.user)
            password_form = PasswordChangeCustomForm(request.user)

    else:
        user_form = UserEditForm(instance=request.user)
        password_form = PasswordChangeCustomForm(request.user)

    return render(request, 'accounts/profile.html', {
        'user_form': user_form,
        'password_form': password_form,
    })
