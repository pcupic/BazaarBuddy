from django.urls import path

from . import views

app_name = 'messenger'

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('<int:pk>/', views.detail, name='detail'),
    path('new-chat/<uuid:product_id>/', views.new_chat, name='new_chat'),
]