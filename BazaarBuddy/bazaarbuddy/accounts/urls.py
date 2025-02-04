from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('profile/', views.profile, name='profile'),  
    path('moderator-dashboard/', views.moderator_dashboard, name="moderator_dashboard"),
    path('approve-moderators/', views.approve_moderators, name='approve_moderators'),
    path('waiting-for-approval/', views.waiting_for_approval, name='waiting_for_approval'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('logout/', views.logout, name="logout"),
    path('proceed-as-regular/', views.proceed_as_regular, name='proceed_as_regular'),
    path('regular-dashboard/', views.regular_dashboard, name="regular_dashboard")
]
