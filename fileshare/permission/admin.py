from guardian.admin import GuardedModelAdmin
from django.utils.translation import gettext as _

from user.admin import fileshare_site

from permission.models import BigUserObjectPermission


class ObjectAdminPermissions(GuardedModelAdmin):
    list_display = ('id', 'object_pk', 'permission')
    search_fields = ('object_pk', 'permission')
    ordering = ('id',)
    readonly_fields = ('id', 'object_pk', 'permission')
    filter_horizontal = ()
    list_filter = ()
    # fieldsets = ((None, {'fields': ('email', 'password')}),
    #              (_('Personal info'), {'fields': ('name', 'about_me', 'date_birth', 'profile_image')}),
    #              (_('Permissions'),
    #               {'fields': ('is_active', 'is_staff',
    #                           'is_superuser')}),
    #              (_('Important dates'), {'fields': ('date_joined', 'last_login')}),
    #              )


fileshare_site.register(BigUserObjectPermission, ObjectAdminPermissions)