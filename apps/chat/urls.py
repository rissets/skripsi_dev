from django.urls import path

from .views import ChatView, UploadPDFView, RenderPDF, TeachableView, TeachableAgentView, CreateTeachableAgent, \
    TestTeachableView, TeachableAgentDeleteView, ChatPDFListView

app_name = "chat"

urlpatterns = [
    path("", ChatView.as_view(), name="index"),
    path("pdfs/", ChatPDFListView.as_view(), name="pdfs"),
    path("upload-pdf/", UploadPDFView.as_view(), name="upload-pdf"),
    path("pdf/<int:pk>/", RenderPDF.as_view(), name="chat-pdf"),
    path("teachable-agent/", TeachableAgentView.as_view(), name="teachable-agent"),
    path("create-teachable-agent/", CreateTeachableAgent.as_view(), name="create-teachable-agent"),
    path("teachable/<str:slug>/", TeachableView.as_view(), name="teachable"),
    path("test-teachable-agent/", TestTeachableView.as_view(), name="test-teachable-agent"),
    path("teachable-agent/<str:slug>/delete/", TeachableAgentDeleteView.as_view(), name="teachable-agent-delete"),
]