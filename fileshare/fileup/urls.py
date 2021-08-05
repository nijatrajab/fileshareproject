from django.urls import path
from . import views

app_name = 'fileup'

urlpatterns = [
    path('', views.FileListView.as_view(), name='list'),
    # path('file/<user_id>/', views.user_file, name='filelist'),
    path('upload/', views.FileUploadView.as_view(), name='upload'),
    path('detail/<int:pk>/', views.FileDetailView.as_view(), name='detail'),
    path('delete/<int:pk>/', views.FileDeleteView.as_view(), name='delete'),
    path('delete-multi/', views.BulkDeleteView.as_view(), name='delete-multi'),
    path('update/<int:pk>/', views.FileUpdateView.as_view(), name='update'),

    path('shared/', views.FileSharedListView.as_view(), name='shared'),
    path('share/<id>/', views.share_file, name='share'),
    path('revoke/<id>/', views.revoke_access, name='revoke'),
    # path('revoke/', views.ra, name='revoke'),

    path('adminpage/', views.AdminPage.as_view(), name='adminpage'),
]
