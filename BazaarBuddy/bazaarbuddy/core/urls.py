from django.urls import path
from django.contrib.auth.views import LoginView
from .forms import LoginForm

app_name = "core"

urlpatterns = [
    path('login/', LoginView.as_view(template_name='core/login.html', authentication_form=LoginForm), name='login'),
]
