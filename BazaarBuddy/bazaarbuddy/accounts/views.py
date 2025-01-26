from django.shortcuts import render, get_object_or_404 ,redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.urls import reverse
from .models import UserProfile
from django.contrib.auth.decorators import user_passes_test


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
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                auth_login(request, user)
                return HttpResponseRedirect(reverse('core:homepage')) 
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")
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

    