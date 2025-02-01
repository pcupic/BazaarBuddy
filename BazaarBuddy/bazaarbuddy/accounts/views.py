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
from django.contrib.admin.views.decorators import staff_member_required
from core.models import Product

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['email']
            user.set_password(form.cleaned_data['password'])
            user.save()

            user_type = form.cleaned_data['user_type']
            user_profile = UserProfile.objects.create(user=user, user_type=user_type)
            
            if user_type == 'moderator':
                user_profile.approval_status = 'pending'
                user_profile.save()

            return redirect('accounts:login')
    else:
        form = RegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})

@staff_member_required  
def approve_moderators(request):
    pending_moderators = UserProfile.objects.filter(user_type='moderator', approval_status='pending')

    if request.method == 'POST':
        user_id = request.POST.get("user_id")
        action = request.POST.get("action")
        user_profile = get_object_or_404(UserProfile, id=user_id)
        
        if action == 'approve':
            user_profile.approval_status = 'approved'
            user_profile.save()
        elif action == 'reject':
            user_profile.approval_status = 'rejected'  
            user_profile.save()

        return redirect('accounts:approve_moderators')  

    return render(request, 'accounts/approve_moderators.html', {'pending_moderators': pending_moderators})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                auth_login(request, user)

                if user.profile.user_type == 'moderator' and user.profile.approval_status == 'pending':
                    return redirect('accounts:waiting_for_approval') 
                
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
            return edit_profile(request)
        
        elif 'change_password' in request.POST:
            return change_password(request)
        
        elif 'logout' in request.POST:
            return logout(request)
        
        elif 'delete_profile' in request.POST:
            return delete_account(request)

    else:
        user_form = UserEditForm(instance=request.user)
        password_form = PasswordChangeForm(request.user)

    return render(request, 'accounts/profile.html', {
        'user_form': user_form,
        'password_form': password_form,
    })

def edit_profile(request):
    user_form = UserEditForm(request.POST, instance=request.user)
    if user_form.is_valid():
        user = user_form.save(commit=False)
        user.username = user.email 
        user.save()
        messages.success(request, "Profile is updated.")
        return redirect('accounts:profile')
    return render(request, 'accounts/profile.html', {'user_form': user_form})

def change_password(request):
    password_form = PasswordChangeForm(request.user, request.POST)
    if password_form.is_valid():
        password_form.save()
        update_session_auth_hash(request, password_form.user)
        messages.success(request, "Your password has been changed.")
        return redirect('accounts:profile')
    return render(request, 'accounts/profile.html', {'password_form': password_form})

def logout(request):
    auth_logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('accounts:login')

def delete_account(request):
    user = request.user
    user.delete()  
    auth_logout(request) 
    messages.success(request, "Your profile has been deleted.")
    return redirect('accounts:login')

@login_required
def moderator_dashboard(request):
    user_profile = request.user.profile
    if user_profile.is_moderator() and not user_profile.is_approved():  
        return redirect('accounts:waiting_for_approval')
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        new_state = request.POST.get("new_state")

        product = get_object_or_404(Product, id=product_id)

        if new_state == Product.State.REJECTED:
            product.delete()  
        else:
            product.state = new_state
            product.save()

        return redirect('accounts:moderator_dashboard')

    pending_products = Product.objects.filter(state=Product.State.PENDING)
    return render(request, 'accounts/moderator_dashboard.html', {'pending_products': pending_products})

# dodati da se prilikom accept ili reject posalje poruka

def waiting_for_approval(request):
    return render(request, 'accounts/waiting_for_approval.html')

@login_required
def proceed_as_regular(request):
    if request.method == "POST":
        user_profile = request.user.profile
        user_profile.user_type = 'regular'
        user_profile.save()
        return redirect('core:home')  