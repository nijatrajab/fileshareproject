from django.contrib import admin
from django.core.cache import cache
from django.core.paginator import Paginator
from guardian.admin import GuardedModelAdmin

from user.admin import fileshare_site

from chat.models import PrivateChatRoom, RoomChatMessage, UnreadChatRoomMessages


class PrivateChatRoomAdmin(GuardedModelAdmin):
    list_display = ['id', 'user1', 'user2', ]
    search_fields = ['id', 'user1__email', 'user2__email', 'user1__name', 'user2__name', ]
    readonly_fields = ['id', ]

    class Meta:
        model = PrivateChatRoom


class CachingPaginator(Paginator):
    def _get_count(self):

        if not hasattr(self, "_count"):
            self._count = None

        if self._count is None:
            try:
                key = "adm:{0}:count".format(hash(self.object_list.query.__str__()))
                self._count = cache.get(key, -1)
                if self._count == -1:
                    self._count = super().count
                    cache.set(key, self._count, 3600)
            except:
                self._count = len(self.object_list)
        return self._count

    count = property(_get_count)


class RoomChatMessageAdmin(GuardedModelAdmin):
    list_filter = ['room', 'user', 'timestamp', ]
    list_display = ['room', 'user', 'content', 'timestamp', ]
    search_fields = ['user__email', 'content', ]
    readonly_fields = ['id', 'user', 'room', 'timestamp']

    show_full_result_count = False
    paginator = CachingPaginator

    class Meta:
        model = RoomChatMessage


class UnreadChatRoomMessagesAdmin(GuardedModelAdmin):
    list_display = ['room', 'user', 'count', ]
    search_fields = ['room__user1__name', 'room__user2__name', ]
    readonly_fields = ['id', ]

    class Meta:
        model = UnreadChatRoomMessages


fileshare_site.register(PrivateChatRoom, PrivateChatRoomAdmin)
fileshare_site.register(RoomChatMessage, RoomChatMessageAdmin)
fileshare_site.register(UnreadChatRoomMessages, UnreadChatRoomMessagesAdmin)
