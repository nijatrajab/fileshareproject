from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'user'

urlpatterns = [
    path('', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('signup/', views.SignUp.as_view(), name='signup'),
]
