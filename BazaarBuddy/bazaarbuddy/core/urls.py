from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path('', views.home, name='homepage'),
    path('products/', views.index, name='index'),
]
