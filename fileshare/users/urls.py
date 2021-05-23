from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    path('', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('signup/', views.SignUp.as_view(), name='signup'),

    path('file_upload/', views.FileUploadView.as_view(), name='file_upload'),
    path('shared_wm/', views.SharedWithMe.as_view(), name='shared_with_me'),
    path('my_files/', views.MyFilesList.as_view(), name='my_files_list'),

    path('detail/<int:pk>', views.FileDetail.as_view(), name='detail'),
    path('delete/<int:pk>', views.UserFilesDeleteView.as_view(), name='delete'),

    path('my_files/share/<id>', views.share_file, name='share'),
    path('detail/revoke/<id>', views.revoke_access, name='revoke'),

    path('adminpage/', views.AdminPage.as_view(), name='adminp'),

]
