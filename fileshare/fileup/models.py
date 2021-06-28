import os
import uuid
import datetime
from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse

from guardian.shortcuts import get_users_with_perms
from fileshare.middleware import get_current_user
from user.models import User


def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return 'user_{0}/{1}'.format(instance.uploaded_by.id, filename)


class UserFile(models.Model):
    title = models.CharField(max_length=50)
    browse_file = models.FileField(upload_to=user_directory_path)
    description = models.CharField(max_length=500, null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    on_delete=models.CASCADE,
                                    related_name='userfile',
                                    blank=True,
                                    null=True,
                                    default=None)

    class Meta:
        default_permissions = ('add', 'change', 'delete')
        permissions = (
            ('view_userfile', 'Can view userfile'),
        )
        get_latest_by = 'uploaded_at'

    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.uploaded_by = user
        if not self.slug:
            self.slug = slugify(self.title)
        return super(UserFile, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('fileup:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

    def extension(self):
        name, extension = os.path.splitext(self.browse_file.name)
        return extension[1:]

    def users_with_perms(self):
        users_with_perms = get_users_with_perms(
            self, only_with_perms_in=['view_userfile']
        )
        return [i for i in users_with_perms if i != self.uploaded_by]

    def users_to_share(self):
        users_with_perms = get_users_with_perms(
            self, only_with_perms_in=['view_userfile'], with_superusers=True
        )
        users_to_share = [user for user in User.objects.all()
                          if user not in users_with_perms]
        return users_to_share

    def admin_page(self):
        users_with_perms = get_users_with_perms(
            self, only_with_perms_in=['view_userfile']
        )
        return [i for i in users_with_perms]

    @property
    def size(self):
        x = self.browse_file.size
        y = 512000
        if x < y:
            value = round(x / 1000, 2)
            ext = ' Kb'
        elif x < y * 1000:
            value = round(x / 1000000, 2)
            ext = ' Mb'
        else:
            value = round(x / 1000000000, 2)
            ext = ' Gb'
        return str(value) + ext