from django.urls import path

from .views import ChatView, ChatPDFView, RenderPDF, TeachableView, TeachableAgentView, CreateTeachableAgent

app_name = "chat"

urlpatterns = [
    path("", ChatView.as_view(), name="index"),
    path("pdf/", ChatPDFView.as_view(), name="pdf"),
    path("<int:pk>/", RenderPDF.as_view(), name="render-pdf"),
    path("teachable-agent/", TeachableAgentView.as_view(), name="teachable-agent"),
    path("create-teachable-agent/", CreateTeachableAgent.as_view(), name="create-teachable-agent"),
    path("teachable/<str:slug>/", TeachableView.as_view(), name="teachable"),
]