from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from guardian.models import UserObjectPermissionAbstract
# from guardian.shortcuts import assign_perm


from notification.models import Notification

from guardian.utils import get_user_obj_perms_model

UserObjectPermission = get_user_obj_perms_model()
from guardian.shortcuts import get_users_with_perms


class BigUserObjectPermission(UserObjectPermissionAbstract):
    id = models.BigAutoField(editable=False, unique=True, primary_key=True)
    timestamp = models.DateTimeField(auto_now=True)

    notifications = GenericRelation(Notification)

    class Meta(UserObjectPermissionAbstract.Meta):
        abstract = False
        indexes = [
            *UserObjectPermissionAbstract.Meta.indexes,
            models.Index(fields=['content_type', 'object_pk', 'user']),
        ]

    def access_notification(self, other_users, file):
        # assign_perm(permission, other_users, file)
        try:
            user_with_perm = get_users_with_perms(
                file, only_with_perms_in=['delete_userfile']
            )
        except:
            pass
        content_type = ContentType.objects.get_for_model(self)
        for other_user in other_users:
            for from_user in user_with_perm:
                self.notifications.create(
                    target=other_user,
                    from_user=from_user,
                    redirect_url=f"{settings.BASE_URL}/user/account/{other_user.pk}/",
                    verb=f"{from_user.name} shared file with title {file.title}",
                    content_type=content_type,
                )
                self.save()

    @property
    def get_cname(self):
        return "FilePermission"
