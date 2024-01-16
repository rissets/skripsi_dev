from django.urls import path

from .views import BackendApi, BackendApiPDF

app_name = "chat-api"

urlpatterns = [
    path("v2/chat/conversation", BackendApi.as_view(), name="backend-api"),
    path("v2/chat/pdf", BackendApiPDF.as_view(), name="backend-api-pdf"),
]