from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Category

def index(request):
    return render(request, 'core/index.html')

def home(request):
    return render(request, 'core/home.html')

def create_product(request):
    return render(request, 'core/create_product.html')