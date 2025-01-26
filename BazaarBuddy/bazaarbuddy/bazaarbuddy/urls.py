from django.contrib import admin
from django.urls import path, include
from core import views


urlpatterns = [
    # path('', views.home, name='homepage'),
    # path('products/', views.index, name='index'),
    # path('products/create/', views.create_product, name="create_product"),

    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('accounts/', include('accounts.urls'))
]
