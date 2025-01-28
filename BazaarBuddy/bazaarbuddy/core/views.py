from django.shortcuts import render, redirect, get_object_or_404, redirect
from .forms import ProductForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Product,Category

@login_required
def index(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    category_id = request.GET.get('category')
    condition = request.GET.get('condition')
    sort = request.GET.get('sort')

    if category_id:
        products = products.filter(category_id = category_id)
    
    if condition:
        products = products.filter(condition = condition)
    
    if sort == "asc":
        products = products.order_by("price")
    elif sort == "desc":
        products = products.order_by("-price")
    
    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'core/index.html', context)
    # products = Product.objects.filter(state = Product.State.ACCEPTED)
    # return render(request, 'core/index.html', {'products': products})

@login_required
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
            messages.success(request, "Product created successfully!")
            return redirect('core:index')
    else:
        form = ProductForm()
    
    return render(request, 'core/create_product.html', {'form': form})

@login_required
def product_detail(request, id):
    product = get_object_or_404(Product, pk = id)
    context = {
        'product': product
    }

    return render(request, 'core/product_detail.html', context)