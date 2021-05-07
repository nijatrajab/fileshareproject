from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('file_upload/', views.FileUploadView.as_view(), name='file_upload'),
    path('all_files/', views.AllFilesList.as_view(), name='all_files_list'),
    path('detail/<slug:slug>/', views.FileDetail.as_view(), name='detail'),
    path('delete/<slug:slug>/', views.UserFilesDeleteView.as_view(), name='delete'),
    # path('my_files/', views.myfiles, name='my_files_list'),
    path('my_files/', views.MyFilesList.as_view(), name='my_files_list'),

    path('my_files/share/<id>', views.share_file, name='share'),
    path('detail/revoke/<id>', views.revoke_access, name='revoke'),

    path('access/', views.Access.as_view(), name='access'),
]
