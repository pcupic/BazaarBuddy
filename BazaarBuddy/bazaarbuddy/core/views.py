from django.shortcuts import render, redirect
from .forms import ProductForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def index(request):
    return render(request, 'core/index.html')

def home(request):
    return render(request, 'core/home.html')

@login_required
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit = False)
            product.user = request.user
            product.save()
            message.success(request, "Product created successfully!")
            return redirect('core:index')
    else:
        form = ProductForm()
    
    return render(request, 'core/create_product.html', {'form': form})