from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, ProductImage, Category
from .forms import ProductForm

def index(request):
    return render(request, 'core/index.html')

def home(request):
    return render(request, 'core/home.html')

# @login_required
def create_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.images = form.cleaned_data['images']
            product.user = request.user
            product.save()
            return redirect('homepage')
        else:
            return render(request, 'core/create_product.html', {'form': form})
    else:
        form = ProductForm()
        return render(request, 'core/create_product.html', {'form': form})
