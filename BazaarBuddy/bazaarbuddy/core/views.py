from django.shortcuts import render, redirect, get_object_or_404, redirect
from .forms import ProductForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Product, Category, Rating

@login_required
def my_posted_products(request):
    products = Product.objects.filter(user = request.user, state__in = [Product.State.PENDING, Product.State.ACCEPTED])

    context = {
        'products': products
    }

    return render(request, 'core/my_posted_products.html', context)

@login_required
def edit_product(request, id):
    product = get_object_or_404(Product, id=id, user=request.user)

    if product.state != "PENDING":
        messages.error(request, "You can only edit products that are pending approval.")
        return redirect('core:my_posted_products')

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully!")
            return redirect('core:my_posted_products')
    else:
        form = ProductForm(instance=product)

    return render(request, 'core/edit_product.html', {'form': form, 'product': product})

@login_required
def delete_product(request, id):
    product = get_object_or_404(Product, id=id, user=request.user)

    if product.state not in ["PENDING", "ACCEPTED"]:
        messages.error(request, "You can only delete pending or accepted products.")
        return redirect('core:my_posted_products')

    product.delete()
    messages.success(request, "Product deleted successfully.")
    return redirect('core:my_posted_products')

@login_required
def index(request):
    products = Product.objects.filter(state=Product.State.ACCEPTED)
    categories = Category.objects.all()

    category_id = request.GET.get('category')
    condition = request.GET.get('condition')
    sort = request.GET.get('sort')

    if category_id:
        products = products.filter(category_id=category_id)

    if condition in dict(Product.Condition.choices):
        products = products.filter(condition=condition)

    if sort == "asc":
        products = products.order_by("price")
    elif sort == "desc":
        products = products.order_by("-price")

    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'core/index.html', context)

@login_required
def home(request):
    return render(request, 'core/home.html')

@login_required
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
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
    product = get_object_or_404(Product, pk=id)
    
    user_rating = Rating.objects.filter(user=request.user, product=product).first()
    user_has_rated = user_rating is not None
    average_rating = product.average_rating()
    
    if request.method == "POST":
        grade_value = int(request.POST.get('grade'))
        if 1 <= grade_value <= 5:
            if user_has_rated:
                user_rating.grade = grade_value
                user_rating.save()
                messages.success(request, "Your rating has been updated!")
            else:
                Rating.objects.create(
                    product=product,
                    user=request.user,
                    grade=grade_value
                )
                messages.success(request, "Your rating has been successfully saved!")
        else:
            messages.error(request, "The rating must be between 1 and 5.")
        return redirect('core:product_detail', id=id)

    context = {
        'product': product,
        'user_has_rated': user_has_rated,
        'user_rating': user_rating, 
        'average_rating': average_rating,
    }
    
    return render(request, 'core/product_detail.html', context)

@login_required
def remove_rating(request, id):
    product = get_object_or_404(Product, pk=id)
    
    user_rating = Rating.objects.filter(user=request.user, product=product).first()
    
    if user_rating:
        user_rating.delete()
        messages.success(request, "Your rating has been removed.")
    else:
        messages.error(request, "You haven't rated this product yet.")
    
    return redirect('core:product_detail', id=id)
