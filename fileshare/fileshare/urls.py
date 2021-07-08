from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from user.admin import fileshare_site
from . import views


handler400 = 'fileshare.views.handler400'
handler403 = 'fileshare.views.handler403'
handler404 = 'fileshare.views.handler404'
handler500 = 'fileshare.views.handler500'
handler503 = 'fileshare.views.handler503'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('fileshareadmin/', fileshare_site.urls),
    path('', views.HomePage.as_view(), name='home'),
    path('user/', include('user.urls', namespace='user')),
    path('user/', include('django.contrib.auth.urls')),
    path('file/', include('fileup.urls', namespace='file')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
