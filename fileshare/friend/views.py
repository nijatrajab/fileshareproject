import json
from django.shortcuts import render, redirect
from django.http import HttpResponse

from user.models import User
from friend.models import FriendRequest, FriendList


def friend_list_view(request, *args, **kwargs):
    context = {}
    user = request.user
    if user.is_authenticated:
        user_id = kwargs.get("user_id")
        if user_id:
            try:
                this_user = User.objects.get(pk=user_id)
                context['this_user'] = this_user
            except User.DoesNotExist:
                return HttpResponse("That user does not exist.")
            try:
                friend_list = FriendList.objects.get(user=this_user)
            except FriendList.DoesNotExist:
                return HttpResponse(f"Could not find a friends list for {this_user.name}")

            if user != this_user:
                if not user in friend_list.friends.all():
                    return HttpResponse(f"You must be friends with {this_user.name} to view friends list ")

            friends = []
            auth_user_friend_list = FriendList.objects.get(user=user)
            for friend in friend_list.friends.all():
                friends.append((friend, auth_user_friend_list.is_mutual_friend(friend)))
            context['friends'] = friends
    else:
        return HttpResponse("You must be friends to view their friend list.")
    return render(request, "friend/friend_list.html", context)



def friend_requests_view(request, *args, **kwargs):
    context = {}
    user = request.user
    if user.is_authenticated:
        user_id = kwargs.get("user_id")
        account = User.objects.get(pk=user_id)
        if account == user:
            friend_requests = FriendRequest.objects.filter(receiver=account, is_active=True)
            context['friend_requests'] = friend_requests
        else:
            return HttpResponse("You can't view another user's friend requests")
    else:
        redirect("login")
    return render(request, "friend/friend_requests.html", context)


def send_friend_request(request, *args, **kwargs):
    user = request.user
    payload = {}

    if request.method == "POST" and user.is_authenticated:
        user_id = request.POST.get("receiver_user_id")
        if user_id:
            receiver = User.objects.get(pk=user_id)
            try:
                friend_request = FriendRequest.objects.filter(sender=user, receiver=receiver)

                # active requests
                try:
                    for request in friend_request:
                        if request.is_active:
                            raise Exception("You already sent them a friend request.")
                        # none active, create new friend request
                    friend_request = FriendRequest(sender=user, receiver=receiver)
                    friend_request.save()
                    payload['response'] = "Friend request sent."
                except Exception as e:
                    payload['response'] = str(e)
            except FriendRequest.DoesNotExist:
                friend_request = FriendRequest(sender=user, receiver=receiver)
                friend_request.save()
                payload['response'] = "Friend request sent."

            if payload['response'] is None:
                payload['response'] = "something went wrong"
        else:
            payload['response'] = "Unable to send a friend request."
    else:
        payload['response'] = "Unable to send a friend request."

    return HttpResponse(json.dumps(payload), content_type="application/json")


def accept_friend_request(request, *args, **kwargs):
    user = request.user
    payload = {}
    if request.method == "GET" and user.is_authenticated:
        friend_request_id = kwargs.get("friend_request_id")
        if friend_request_id:
            friend_request = FriendRequest.objects.get(pk=friend_request_id)
            if friend_request.receiver == user:
                if friend_request:
                    friend_request.accept()
                    payload['response'] = "Friend request accepted."
                else:
                    payload['response'] = "Something went wrong."
            else:
                payload['response'] = "That is not your request to accept."
        else:
            payload['response'] = "unable to accept that friend request."
    else:
        payload['response'] = "You must be authenticated to accept a friend request."

    return HttpResponse(json.dumps(payload), content_type='application/json')


def remove_friend(request, *args, **kwargs):
    user = request.user
    payload = {}
    if request.method == "POST" and user.is_authenticated:
        user_id = request.POST.get("receiver_user_id")
        if user_id:
            try:
                removee = User.objects.get(pk=user_id)
                friend_list = FriendList.objects.get(user=user)
                friend_list.unfriend(removee)
                payload['response'] = "Successfully removed that friend."
            except Exception as e:
                payload['response'] = f"Something went wrong: {str(e)}"
        else:
            payload['response'] = "There was an error. Unable to remove that friend."
    else:
        payload['response'] = "You must be authenticated to remove a friend."
    return HttpResponse(json.dumps(payload), content_type="application/json")


def decline_friend_request(request, *args, **kwargs):
    user = request.user
    payload = {}

    if request.method == "GET" and user.is_authenticated:
        friend_request_id = kwargs.get("friend_request_id")
        if friend_request_id:
            friend_request = FriendRequest.objects.get(pk=friend_request_id)
            if friend_request.receiver == user:
                if friend_request:
                    friend_request.decline()
                    payload['response'] = "Friend request decline."
                else:
                    payload['response'] = "Something went wrong."
            else:
                payload['response'] = "That is not your friend request to decline."
        else:
            payload['response'] = "Unable to decline that friend request decline."
    else:
        payload['response'] = "You must be authenticated to decline friend request."
    return HttpResponse(json.dumps(payload), content_type="application/json")


def cancel_friend_request(request, *args, **kwargs):
    user = request.user
    payload = {}
    if request.method == "POST" and user.is_authenticated:
        user_id = request.POST.get("receiver_user_id")
        if user_id:
            receiver = User.objects.get(pk=user_id)
            try:
                friend_requests = FriendRequest.objects.filter(sender=user, receiver=receiver, is_active=True)
            except Exception as e:
                payload['response'] = "Nothing to cancel. Friend request does not exist."

            if len(friend_requests) > 1:
                for request in friend_requests:
                    request.cancel()
                payload['response'] = "Friend requests cancelled."
            else:
                friend_requests.first().cancel()
                payload['response'] = "Friend request cancelled."
        else:
            payload['response'] = "Unable to cancel that friend request."
    else:
        payload['response'] = "You must be authenticated to cancel a friend request."
    return HttpResponse(json.dumps(payload), content_type="application/json")
