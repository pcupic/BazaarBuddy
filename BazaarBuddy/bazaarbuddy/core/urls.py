from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path('', views.home, name='homepage'),
    path('products/', views.index, name='index'),
    path('products/create/', views.create_product, name='create_product'),
    path('product/<uuid:id>/', views.product_detail, name="product_detail"),
    path('products/my-listing/',views.my_posted_products, name='my_posted_products'),
    path('product/<uuid:id>/remove_rating/', views.remove_rating, name='remove_rating'),
]
