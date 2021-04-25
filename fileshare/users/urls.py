from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('file_upload/', views.FileUploadView.as_view(), name='file_upload'),
    path('all_files/', views.FilesList.as_view(), name='all_files_list'),
    path('my_files/', views.MyFilesList.as_view(), name='my_files_list'),
    path('detail/<slug:slug>/', views.FileDetail.as_view(), name='detail'),
    path('delete/<int:id>/', views.FileDeleteView, name='delete'),
    # path('share/<int:id>/', views.user_gains_perms, name='share'),
]
