from django.urls import path

from . import views

app_name = "friend"

urlpatterns = [
    path('friend_request/', views.send_friend_request, name="friend-request"),
    path('friend_request/<user_id>/', views.friend_requests_view, name="friend_requests"),
    path('friend_request_accept/<friend_request_id>/', views.accept_friend_request,
         name="friend_request_accept"),
    path('friend_remove/', views.remove_friend, name="friend_remove"),
    path('friend_request_decline/<friend_request_id>', views.decline_friend_request,
         name="friend_request_decline"),
    path('friend_request_cancel/', views.cancel_friend_request, name="friend_request_cancel"),
    path('friend_list/<user_id>/', views.friend_list_view, name="friend_list"),
]
