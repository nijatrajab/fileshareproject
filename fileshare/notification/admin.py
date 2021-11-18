from guardian.admin import GuardedModelAdmin

from user.admin import fileshare_site
from notification.models import Notification


class NotificationAdmin(GuardedModelAdmin):

    list_filter = ['content_type']
    list_display = ['target', 'content_type', 'timestamp']
    search_fields = ['target__name', 'target__email']

    class Meta:
        model = Notification


fileshare_site.register(Notification, NotificationAdmin)