from django.contrib import admin
from .models import Category, User, Product

admin.site.register(Category)
admin.site.register(Product)