from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from user.admin import fileshare_site
from . import views

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('fileshareadmin/', fileshare_site.urls),
                  path('', views.HomePage.as_view(), name='home'),
                  path('user/', include('user.urls', namespace='user')),
                  path('user/', include('django.contrib.auth.urls')),
                  path('file/', include('fileup.urls', namespace='file')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
