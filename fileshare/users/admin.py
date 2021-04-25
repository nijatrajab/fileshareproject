from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from django.contrib.auth.models import Group
from django.contrib import messages

from guardian.admin import GuardedModelAdmin

from .models import User, UserFiles
from .forms import UserCreationForm, UserChangeForm


class FileShareAdminArea(admin.AdminSite):
    site_header = 'FileShare Database'


class TestAdminPermissions(GuardedModelAdmin):
    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        if obj != None and request.POST.get('action') == 'delete_selected':
            messages.add_message(request, messages.ERROR, (
                'Are you sure?'
            ))
        return obj is None or obj.id != 13

    def has_view_permission(self, request, obj=None):
        return True


fileshare_site = FileShareAdminArea(name='FileShareAdmin')


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    ordering = ('id',)
    list_display = ['email', 'name', 'is_staff']
    fieldsets = ((None, {'fields': ('email', 'password')}),
                 (_('Personal info'), {'fields': ('name',)}),
                 (_('Permissions'),
                  {'fields': ('is_active', 'is_staff', 'is_superuser', 'has_perm')}),
                 (_('Important dates'), {'fields': ('last_login',)}),
                 )
    add_fieldsets = ((None, {'classes': ('wide',),
                             'fields': ('email', 'name',
                                        'password1', 'password2'), }),)


fileshare_site.register(User, TestAdminPermissions)
fileshare_site.register(UserFiles, TestAdminPermissions)
fileshare_site.register(Group, TestAdminPermissions)
