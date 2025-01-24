from django.contrib import admin
from django.urls import path
from core import views


urlpatterns = [
    path('products/', views.index, name='index'),
    path('', views.home, name='homepage'),
    path('admin/', admin.site.urls),
]
