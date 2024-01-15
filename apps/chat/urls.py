from django.urls import path

from .views import ChatView, BackendApi

app_name = "chat"

urlpatterns = [
    path("", ChatView.as_view(), name="index"),
    path("backend-api/v2/conversation", BackendApi.as_view(), name="backend-api"),
]