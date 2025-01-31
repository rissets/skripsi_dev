
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from .views import DashboardView

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path("admin/", admin.site.urls),
    path("chat/", include("chat.urls", namespace="chat")),
    path("api/", include("chat.api.urls", namespace="chat-api")),

]
               # + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
