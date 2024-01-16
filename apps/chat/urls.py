from django.urls import path

from .views import ChatView, ChatPDFView, RenderPDF

app_name = "chat"

urlpatterns = [
    path("", ChatView.as_view(), name="index"),
    path("pdf/", ChatPDFView.as_view(), name="pdf"),
    path("<int:pk>/", RenderPDF.as_view(), name="render-pdf"),
    # path("backend-api/v2/conversation", BackendApi.as_view(), name="backend-api"),
]