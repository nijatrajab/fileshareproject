from django.urls import path
from . import views

app_name = 'fileup'

urlpatterns = [
    path('fileupload/', views.FileUploadView.as_view(), name='file_upload'),
    path('shared/', views.SharedWithMe.as_view(), name='shared_with_me'),
    path('myfiles/', views.MyFilesList.as_view(), name='my_files_list'),

    path('detail/<int:pk>', views.FileDetail.as_view(), name='detail'),
    path('delete/<int:pk>', views.FileDeleteView.as_view(), name='delete'),

    path('myfiles/share/<id>', views.share_file, name='share'),
    path('detail/revoke/<id>', views.revoke_access, name='revoke'),

    path('adminpage/', views.AdminPage.as_view(), name='adminpage'),
]
