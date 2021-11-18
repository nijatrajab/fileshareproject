from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.utils import timezone

from chat.utils import find_or_create_private_chat
from notification.models import Notification


class FriendList(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user")
    friends = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="friends")

    notifications = GenericRelation(Notification)

    def __str__(self):
        return self.user.name

    def add_friend(self, account):
        if account not in self.friends.all():
            self.friends.add(account)

            content_type = ContentType.objects.get_for_model(self)

            self.notifications.create(
                target=self.user,
                from_user=account,
                redirect_url=f"{settings.BASE_URL}/user/account/{account.pk}/",
                verb=f"You are now friends with {account.name}",
                content_type=content_type,
            )
            self.save()

            chat = find_or_create_private_chat(self.user, account)
            if not chat.is_active:
                chat.is_active = True
                chat.save()

    def remove_friend(self, account):
        if account in self.friends.all():
            self.friends.remove(account)

            chat = find_or_create_private_chat(self.user, account)
            if chat.is_active:
                chat.is_active = False
                chat.save()

    def unfriend(self, removee):
        """
        Unfriending someone
        remover - the person who is terminating friendship
        removee - the person who is getting removed
        """

        remover_friends_list = self

        # Remove friend from remover friend list
        remover_friends_list.remove_friend(removee)

        # Remove friend from removee friend list
        friends_list = FriendList.objects.get(user=removee)
        friends_list.remove_friend(self.user)

        content_type = ContentType.objects.get_for_model(self)

        self.notifications.create(
            target=removee,
            from_user=self.user,
            redirect_url=f"{settings.BASE_URL}/user/account/{self.user.pk}/",
            verb=f"You are no longer friends with {self.user.name}",
            content_type=content_type,
        )

        self.notifications.create(
            target=self.user,
            from_user=removee,
            redirect_url=f"{settings.BASE_URL}/user/account/{removee.pk}/",
            verb=f"You are no longer friends with {removee.name}",
            content_type=content_type,
        )

        self.save()

    def is_mutual_friend(self, friend):
        if friend in self.friends.all():
            return True
        return False

    @property
    def get_cname(self):
        return "FriendList"


class FriendRequest(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="receiver")

    is_active = models.BooleanField(blank=True, null=False, default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    notifications = GenericRelation(Notification)

    def __str__(self):
        return self.sender.name

    def accept(self):
        """
        Accept a friend request + update sender and receiver friend list
        """
        receiver_friend_list = FriendList.objects.get(user=self.receiver)
        if receiver_friend_list:

            content_type = ContentType.objects.get_for_model(self)

            receiver_notification = Notification.objects.get(target=self.receiver,
                                                             content_type=content_type,
                                                             object_id=self.pk)
            receiver_notification.is_active = False
            receiver_notification.redirect_url = f"{settings.BASE_URL}/user/account/{self.sender.pk}/"
            receiver_notification.verb = f"You accepted {self.sender.name}'s friend request."
            receiver_notification.timestamp = timezone.now()
            receiver_notification.save()

            receiver_friend_list.add_friend(self.sender)

            sender_friend_list = FriendList.objects.get(user=self.sender)
            if sender_friend_list:

                self.notifications.create(
                    target=self.sender,
                    from_user=self.receiver,
                    redirect_url=f"{settings.BASE_URL}/user/account/{self.receiver.pk}/",
                    verb=f"{self.receiver.name} accepted your friend request.",
                    content_type=content_type,
                )

                sender_friend_list.add_friend(self.receiver)
                self.is_active = False
                self.save()

            return receiver_notification

    def decline(self):
        """
        Decline a friend request is change "is_active" field to False
        """
        self.is_active = False
        self.save()

        content_type = ContentType.objects.get_for_model(self)

        receiver_notification = Notification.objects.get(target=self.receiver,
                                                         content_type=content_type,
                                                         object_id=self.pk)
        receiver_notification.is_active = False
        receiver_notification.redirect_url = f"{settings.BASE_URL}/user/account/{self.sender.pk}/"
        receiver_notification.verb = f"You declined {self.sender.name}'s friend request."
        receiver_notification.timestamp = timezone.now()
        receiver_notification.save()

        self.notifications.create(
            target=self.sender,
            from_user=self.receiver,
            redirect_url=f"{settings.BASE_URL}/user/account/{self.receiver.pk}/",
            verb=f"{self.receiver.name} declined your friend request.",
            content_type=content_type,
        )

        return receiver_notification

    def cancel(self):
        """
        Cancel a friend request is change "is_active" field to False
        """
        self.is_active = False
        self.save()

        content_type = ContentType.objects.get_for_model(self)

        receiver_notification = Notification.objects.get(target=self.receiver,
                                                         content_type=content_type,
                                                         object_id=self.pk)
        receiver_notification.is_active = False
        receiver_notification.redirect_url = f"{settings.BASE_URL}/user/account/{self.sender.pk}/"
        receiver_notification.verb = f"{self.sender.name} cancelled friend request sent to you."
        receiver_notification.save()

        self.notifications.create(
            target=self.sender,
            from_user=self.receiver,
            redirect_url=f"{settings.BASE_URL}/user/account/{self.receiver.pk}/",
            verb=f"You cancelled your friend request to {self.receiver.name}.",
            content_type=content_type,
        )

    @property
    def get_cname(self):
        return "FriendRequest"


@receiver(post_save, sender=FriendRequest)
def create_notification(sender, instance, created, **kwargs):
    if created:
        instance.notifications.create(
            target=instance.receiver,
            from_user=instance.sender,
            redirect_url=f"{settings.BASE_URL}/user/account/{instance.sender.pk}",
            verb=f"{instance.sender.name} sent you a friend request.",
            content_type=instance,
        )