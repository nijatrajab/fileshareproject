import json
from datetime import datetime

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator

from chat.models import UnreadChatRoomMessages
from friend.models import FriendRequest, FriendList
from .models import Notification
from .utils import LazyNotificationEncoder
from .constants import *
from chat.exceptions import ClientError


class NotificationConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        print("notificationconsumer: connect: " + str(self.scope['user']))
        await self.accept()

    async def disconnect(self, code):
        print("notificationconsumer: disconnect")

    async def receive_json(self, content, **kwargs):
        command = content.get("command", None)
        print("notificationconsumer: receive__json. command: " + command)
        try:
            if command == "get_general_notifications":
                payload = await get_general_notifications(self.scope['user'], content['page_number'])
                if payload is None:
                    await self.general_pagination_exhausted()
                else:
                    payload = json.loads(payload)
                    await self.send_general_notifications_payload(payload['notifications'], payload['new_page_number'])

            elif command == "accept_friend_request":
                notification_id = content['notification_id']
                payload = await accept_friend_request(self.scope['user'], notification_id)
                if payload is None:
                    raise ClientError(204, "Something went wrong. Try refresh page")
                else:
                    payload = json.loads(payload)
                    await self.send_updated_friend_request_notification(payload['notification'])

            elif command == "decline_friend_request":
                notification_id = content['notification_id']
                payload = await decline_friend_request(self.scope['user'], notification_id)
                if payload is None:
                    raise ClientError(204, "Something went wrong. Try refresh page")
                else:
                    payload = json.loads(payload)
                    await self.send_updated_friend_request_notification(payload['notification'])

            elif command == "refresh_general_notifications":
                payload = await refresh_general_notifications(self.scope['user'], content['oldest_timestamp'],
                                                              content['newest_timestamp'])
                if payload is None:
                    raise ClientError(204, "Something went wrong. Try refresh page")
                else:
                    payload = json.loads(payload)
                    await self.send_general_refreshed_notifications_payload(payload['notifications'])

            elif command == "get_new_general_notifications":
                payload = await get_new_general_notifications(self.scope['user'], content.get("newest_timestamp", None))
                print(self.scope['user'], content.get("newest_timestamp", None), payload)
                if payload is not None:
                    payload = json.loads(payload)
                    await self.send_new_general_notifications_payload(payload['notifications'])

            elif command == "get_unread_general_notifications_count":
                payload = await get_unread_general_notifications_count(self.scope['user'])
                if payload is not None:
                    payload = json.loads(payload)
                    await self.send_unread_general_notification_count(payload['count'])

            elif command == "mark_notifications_read":
                await mark_notifications_read(self.scope['user'])

            elif command == "get_chat_notifications":
                payload = await get_chat_notifications(self.scope['user'], content.get('page_number', None))
                if payload is None:
                    await self.chat_pagination_exhausted()
                else:
                    payload = json.loads(payload)
                    await self.send_chat_notifications_payload(payload['notifications'], payload['new_page_number'])

            elif command == "get_new_chat_notifications":
                payload = await get_new_chat_notifications(self.scope['user'], content.get('newest_timestamp', None))
                if payload is not None:
                    payload = json.loads(payload)
                    await self.send_new_chat_notifications_payload(payload['notifications'])

            elif command == "get_unread_chat_notifications_count":
                payload = await get_unread_chat_notification_count(self.scope['user'])
                if payload is not None:
                    payload = json.loads(payload)
                    await self.send_unread_chat_notification_count(payload['count'])

        except ClientError as e:
            print("EXCEPTION ON NOTIF: " + str(e))

    async def display_progress_bar(self, shouldDisplay):
        print("notificationconsume: display_progress_bar: " + str(shouldDisplay))
        await self.send_json(
            {
                "progress_bar": shouldDisplay
            }
        )

    async def send_general_notifications_payload(self, notifications, new_page_number):
        await self.send_json({
            'general_msg_type': GENERAL_MSG_TYPE_NOTIFICATIONS_PAYLOAD,
            'notifications': notifications,
            'new_page_number': new_page_number
        })

    async def send_updated_friend_request_notification(self, notification):
        await self.send_json({
            "general_msg_type": GENERAL_MSG_TYPE_UPDATED_NOTIFICATION,
            "notification": notification
        })

    async def general_pagination_exhausted(self):
        await self.send_json({
            "general_msg_type": GENERAL_MSG_TYPE_PAGINATION_EXHAUSTED,
        })

    async def send_general_refreshed_notifications_payload(self, notifications):
        await self.send_json({
            "general_msg_type": GENERAL_MSG_TYPE_NOTIFICATIONS_REFRESH_PAYLOAD,
            "notifications": notifications
        })

    async def send_new_general_notifications_payload(self, notifications):
        await self.send_json({
            "general_msg_type": GENERAL_MSG_TYPE_GET_NEW_NOTIFICATIONS,
            "notifications": notifications
        }, )

    async def send_unread_general_notification_count(self, count):
        await self.send_json({
            "general_msg_type": GENERAL_MSG_TYPE_GET_UNREAD_NOTIFICATIONS_COUNT,
            "count": count
        })

    async def send_chat_notifications_payload(self, notifications, new_page_number):
        await self.send_json({
            "chat_msg_type": CHAT_MSG_TYPE_NOTIFICATIONS_PAYLOAD,
            "notifications": notifications,
            "new_page_number": new_page_number
        })

    async def send_new_chat_notifications_payload(self, notifications):
        await self.send_json({
            "chat_msg_type": CHAT_MSG_TYPE_NEW_NOTIFICATIONS,
            "notifications": notifications
        })

    async def chat_pagination_exhausted(self):
        await self.send_json({
            "chat_msg_type": CHAT_MSG_TYPE_PAGINATION_EXHAUSTED
        })

    async def send_unread_chat_notification_count(self, count):
        await self.send_json({
            "chat_msg_type": CHAT_MSG_TYPE_UNREAD_NOTIFICATIONS_COUNT,
            "count": count
        })


@database_sync_to_async
def get_general_notifications(user, page_number):
    if user.is_authenticated:
        friend_request_ct = ContentType.objects.get_for_model(FriendRequest)
        friend_list_ct = ContentType.objects.get_for_model(FriendList)
        notifications = Notification.objects.filter(target=user, content_type__in=[
            friend_request_ct, friend_list_ct]).order_by("-timestamp")
        p = Paginator(notifications, DEFAULT_NOTIFICATION_PAGE_SIZE)

        payload = {}
        if len(notifications) > 0:
            if int(page_number) <= p.num_pages:
                s = LazyNotificationEncoder()
                serialized_notifications = s.serialize(p.page(page_number).object_list)
                payload['notifications'] = serialized_notifications
                new_page_number = int(page_number) + 1
                payload['new_page_number'] = new_page_number
                return json.dumps(payload)
        else:
            return None
    else:
        raise ClientError("AUTHENTICATION_ERROR", "User must be authenticated to get notifications.")
    return None


@database_sync_to_async
def accept_friend_request(user, notification_id):
    payload = {}
    if user.is_authenticated:
        try:
            notification = Notification.objects.get(pk=notification_id)
            friend_request = notification.content_object
            if friend_request.receiver == user:
                updated_notification = friend_request.accept()
                s = LazyNotificationEncoder()
                payload['notification'] = s.serialize([updated_notification])[0]
                return json.dumps(payload)
        except Notification.DoesNotExist:
            raise ClientError(422, "An error occurred with that notification. Try refresh page")
        return None


@database_sync_to_async
def decline_friend_request(user, notification_id):
    payload = {}
    if user.is_authenticated:
        try:
            notification = Notification.objects.get(pk=notification_id)
            friend_request = notification.content_object
            if friend_request.receiver == user:
                updated_notification = friend_request.decline()
                s = LazyNotificationEncoder()
                payload['notification'] = s.serialize([updated_notification])[0]
                return json.dumps(payload)
        except Notification.DoesNotExist:
            raise ClientError(422, "An error occurred with that notification. Try refresh page")
        return None


@database_sync_to_async
def refresh_general_notifications(user, oldest_timestamp, newest_timestamp):
    payload = {}
    if user.is_authenticated:
        oldest_ts = oldest_timestamp[0:oldest_timestamp.find("+")]
        if oldest_ts != '':
            oldest_ts = datetime.strptime(oldest_ts, "%Y-%m-%d %H:%M:%S.%f")

        newest_ts = newest_timestamp[0:newest_timestamp.find("+")]
        if newest_ts != '':
            newest_ts = datetime.strptime(newest_ts, "%Y-%m-%d %H:%M:%S.%f")

        friend_request_ct = ContentType.objects.get_for_model(FriendRequest)
        friend_list_ct = ContentType.objects.get_for_model(FriendList)

        notifications = Notification.objects.filter(target=user,
                                                    content_type__in=[friend_request_ct, friend_list_ct],
                                                    timestamp__gte=oldest_ts,
                                                    timestamp__lte=newest_ts).order_by("-timestamp")

        s = LazyNotificationEncoder()
        payload['notifications'] = s.serialize(notifications)
        return json.dumps(payload)
    else:
        raise ClientError(204, "User must be authenticated to get notifications")
    return None


@database_sync_to_async
def get_new_general_notifications(user, newest_timestamp):
    payload = {}
    if user.is_authenticated:
        timestamp = newest_timestamp[0:newest_timestamp.find("+")]
        if timestamp != '':
            timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")

        friend_request_ct = ContentType.objects.get_for_model(FriendRequest)
        friend_list_ct = ContentType.objects.get_for_model(FriendList)

        notifications = Notification.objects.filter(target=user,
                                                    content_type__in=[friend_request_ct, friend_list_ct],
                                                    timestamp__gt=timestamp,
                                                    read=False).order_by("-timestamp")

        s = LazyNotificationEncoder()
        payload['notifications'] = s.serialize(notifications)
        return json.dumps(payload)
    else:
        raise ClientError(204, "User must be authenticated to get notifications")
    return None


@database_sync_to_async
def get_unread_general_notifications_count(user):
    payload = {}
    if user.is_authenticated:
        friend_request_ct = ContentType.objects.get_for_model(FriendRequest)
        friend_list_ct = ContentType.objects.get_for_model(FriendList)

        notifications = Notification.objects.filter(target=user,
                                                    content_type__in=[friend_request_ct, friend_list_ct],
                                                    read=False)
        unread_count = 0
        if notifications:
            for notification in notifications:
                if not notification.read:
                    unread_count = unread_count + 1
        payload['count'] = unread_count
        return json.dumps(payload)
    else:
        raise ClientError(204, "User must be authenticated!")
    return None


@database_sync_to_async
def mark_notifications_read(user):
    if user.is_authenticated:
        notifications = Notification.objects.filter(target=user)
        if notifications:
            for notification in notifications:
                notification.read = True
                notification.save()
    return


@database_sync_to_async
def get_chat_notifications(user, page_number):
    payload = {}
    if user.is_authenticated:
        chat_message_ct = ContentType.objects.get_for_model(UnreadChatRoomMessages)
        notifications = Notification.objects.filter(target=user,
                                                    content_type=chat_message_ct).order_by("-timestamp")
        p = Paginator(notifications, DEFAULT_NOTIFICATION_PAGE_SIZE)

        if len(notifications) > 0:
            if int(page_number) <= p.num_pages:
                s = LazyNotificationEncoder()
                serialized_notifications = s.serialize(p.page(page_number).object_list)
                payload['notifications'] = serialized_notifications
                new_page_number = int(page_number) + 1
                payload['new_page_number'] = new_page_number
                return json.dumps(payload)
        else:
            return None
    else:
        raise ClientError(204, "User must be authenticated!")
    return None


@database_sync_to_async
def get_new_chat_notifications(user, newest_timestamp):
    payload = {}
    if user.is_authenticated:
        timestamp = newest_timestamp[0:newest_timestamp.find("+")]
        if timestamp != '':
            timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")

        chat_message_ct = ContentType.objects.get_for_model(UnreadChatRoomMessages)
        notifications = Notification.objects.filter(target=user,
                                                    content_type=chat_message_ct,
                                                    timestamp__gt=timestamp).order_by("-timestamp")
        s = LazyNotificationEncoder()
        payload['notifications'] = s.serialize(notifications)
        return json.dumps(payload)
    else:
        ClientError("AUTH_ERROR", "User must be authenticated!")
    return None


@database_sync_to_async
def get_unread_chat_notification_count(user):
    payload = {}

    if user.is_authenticated:
        chat_message_ct = ContentType.objects.get_for_model(UnreadChatRoomMessages)
        notifications = Notification.objects.filter(target=user,
                                                    content_type=chat_message_ct)
        unread_count = 0
        if notifications:
            unread_count = len(notifications.all())
        payload['count'] = unread_count
        return json.dumps(payload)
    else:
        ClientError("AUTH_ERROR", "User must be authenticated!")
    return None
