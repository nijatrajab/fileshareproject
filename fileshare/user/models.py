import datetime
import os
import random

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import (BaseUserManager,
                                        AbstractBaseUser,
                                        PermissionsMixin)


from fileshare import settings
from imagekit.models import ImageSpecField
from imagekit.processors import SmartResize


def get_profile_image_filepath(self, filename):
    return f'profile_images/user_{self.pk}/{"profile_image.png"}'


def get_default_profile_image_filepath():
    random_image = random.choice([
        x for x in os.listdir(settings.RANDOM_AVATAR)
    ])
    return os.path.join('fs_default/', random_image)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email please')

        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def __str__(self):
        return self.email


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=50, unique=True, verbose_name='email address')
    name = models.CharField(max_length=255)
    date_birth = models.DateField(verbose_name='birth date', null=True, blank=True)
    about_me = models.CharField(max_length=144, null=True, blank=True, )
    date_joined = models.DateTimeField(verbose_name='data joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    profile_image = models.ImageField(max_length=255, null=True, blank=True,
                                      upload_to=get_profile_image_filepath, default=get_default_profile_image_filepath)
    profile_image_thumb = ImageSpecField(source='profile_image', processors=[SmartResize(54, 54)], format="PNG")
    profile_image_detail_thumb = ImageSpecField(source='profile_image', processors=[SmartResize(250, 250)],
                                                format="PNG")

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def natural_key(self):
        return self.email

    def get_profile_image_filename(self):
        return str(self.profile_image)[str(self.profile_image).index(f'profile_images/{self.pk}/'):]

    def get_absolute_url(self):
        return reverse('user:account', kwargs={'user_id': self.pk})

    # def save(self, *args, **kwargs):
    #     if self.date_birth > datetime.date.today():
    #         raise ValidationError("Select correct date birth")
    #     super(User, self).save(*args, *kwargs)

    def __str__(self):
        return self.email


from guardian.models import UserObjectPermissionAbstract
from guardian.utils import get_user_obj_perms_model


class BigUserObjectPermission(UserObjectPermissionAbstract):
    id = models.BigAutoField(editable=False, unique=True, primary_key=True)
    timestamp = models.DateTimeField(auto_now=True)

    class Meta(UserObjectPermissionAbstract.Meta):
        abstract = False
        indexes = [
            *UserObjectPermissionAbstract.Meta.indexes,
            models.Index(fields=['content_type', 'object_pk', 'user']),
        ]


UserObjectPermission = get_user_obj_perms_model()
