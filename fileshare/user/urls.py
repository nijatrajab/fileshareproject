from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'user'

urlpatterns = [
    path('', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('validate_username/', views.validate_username, name='validate_username'),
]
