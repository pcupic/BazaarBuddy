from django.contrib import admin
from django.urls import path, include
from core import views


urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('core/', include('core.urls'))
]
