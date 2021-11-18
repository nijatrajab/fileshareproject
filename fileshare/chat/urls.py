from django.urls import path

from . import views

app_name = 'chat'


urlpatterns = [
    path('', views.private_chat_room_view, name='private_chat_room'),
    path('corpc/', views.create_or_return_private_chat, name='cor_private_chat'),
]