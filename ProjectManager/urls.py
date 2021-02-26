from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('account/', include("accounts.urls", namespace="accounts")),
    path("api/", include("api.urls", namespace="api")),
    path('admin/', admin.site.urls),
    path('', include("core.urls", namespace="core")),
    path('ckeditor/', include("ckeditor_uploader.urls"))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'core.views.handler404'
