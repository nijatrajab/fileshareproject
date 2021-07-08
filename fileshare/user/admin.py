from django.contrib import admin
from django.utils.translation import gettext as _

from guardian.admin import GuardedModelAdmin

from .models import User
from fileup.models import UserFile


class FileShareAdminArea(admin.AdminSite):
    site_header = 'FileShare Admin'


class FileAdminPermissions(GuardedModelAdmin):
    list_display = ('title', 'uploaded_by', 'uploaded_at', 'modified_at')
    search_fields = ('title', 'uploaded_by')
    ordering = ('id',)
    readonly_fields = ('id', 'uploaded_by', 'uploaded_at', 'modified_at', 'browse_file')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ((_('File info'), {'fields': ('title', 'description', 'uploaded_by')}),
                 (_('Download'), {'fields': ('browse_file',)}),
                 (_('Important dates'), {'fields': ('uploaded_at', 'modified_at')}),
                 )


class UserAdminPermissions(GuardedModelAdmin):
    list_display = ('email', 'name', 'date_birth', 'date_joined', 'last_login', 'is_staff')
    search_fields = ('email', 'name')
    ordering = ('id',)
    readonly_fields = ('id', 'date_joined', 'last_login')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ((None, {'fields': ('email', 'password')}),
                 (_('Personal info'), {'fields': ('name', 'about_me', 'date_birth', 'profile_image')}),
                 (_('Permissions'),
                  {'fields': ('is_active', 'is_staff',
                              'is_superuser')}),
                 (_('Important dates'), {'fields': ('date_joined', 'last_login')}),
                 )


fileshare_site = FileShareAdminArea(name='FileShareAdmin')

fileshare_site.register(User, UserAdminPermissions)
fileshare_site.register(UserFile, FileAdminPermissions)
# fileshare_site.register(Group,)
