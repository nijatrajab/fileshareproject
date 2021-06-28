from .models import UserFile
from django.db.models import Q
from django.http import JsonResponse


class ShareMixin(object):
    def get_queryset(self):
        return UserFile.objects.filter(~Q(uploaded_by=self.request.user))




