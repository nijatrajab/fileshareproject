import uuid
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (BaseUserManager,
                                        AbstractBaseUser,
                                        PermissionsMixin)
from fileshare.middleware import get_current_user
from django.template.defaultfilters import slugify
from django.urls import reverse


def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return 'user_{0}/{1}'.format(instance.uploaded_by.id, filename)


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email yaz!')

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
    email = models.EmailField(max_length=50,
                              unique=True,
                              verbose_name='email address')
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email


class UserFiles(models.Model):
    title = models.CharField(max_length=50)
    browse_file = models.FileField(upload_to=user_directory_path)
    description = models.CharField(max_length=500, null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    on_delete=models.CASCADE,
                                    related_name='userfiless',
                                    blank=True,
                                    null=True,
                                    default=None)

    class Meta:
        default_permissions = ('add', 'change', 'delete')
        permissions = (
            ('view_userfiles', 'Can view userfiles'),
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
        return super(UserFiles, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title
