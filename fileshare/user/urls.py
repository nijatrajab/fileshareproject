from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'user'

urlpatterns = [
    # authenticate urls
    path('', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('login/', views.LgnView.as_view(), name='login'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('validate_email/', views.validate_email_regex, name='validate_email'),

    # password urls
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='password/password_change_done.html'),
         name='password_change_done'),
    path('password_change/', views.PassChangeView.as_view(), name='password_change'),
    path('password_reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'),
         name='password_reset_complete'),
    path('reset/uidb64/<token>/',
         auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/',
         auth_views.PasswordResetView.as_view(), name='password_reset'),

    # user urls
    path('account/<user_id>/', views.account_view, name='account'),
    path('account/<user_id>/edit', views.account_edit_view, name='account_edit'),
    path('account/<user_id>/edit/crop_image', views.crop_image, name='crop_image'),
    path('search_u/', views.account_search_view, name='search_user'),

]
