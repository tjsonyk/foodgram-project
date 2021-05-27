from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404, handler500

from . import views

handler404 = 'foodgram.views.page_not_found'
handler500 = 'foodgram.views.server_error'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('personal/auth/', include('django.contrib.auth.urls')),
    path('personal/', include('users.urls', namespace='users')), 
    path('', include('recipes.urls')),
    path('project/', views.JustStaticPage.as_view(), name='technologies')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
