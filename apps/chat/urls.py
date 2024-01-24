from django.urls import path

from .views import ChatView, UploadPDFView, RenderPDF, TeachableView, TeachableAgentView, CreateTeachableAgent, \
    TestTeachableView, TeachableAgentDeleteView, ChatPDFListView, ChatPDFDeleteView, GroupChatListView, GroupChatCreateView, \
    AgentView, AgentCreateView, AgentDeleteView, AgentUpdateView, GroupChatView


app_name = "chat"

urlpatterns = [
    path("", ChatView.as_view(), name="index"),

    path("pdfs/", ChatPDFListView.as_view(), name="pdfs"),
    path("upload-pdf/", UploadPDFView.as_view(), name="upload-pdf"),
    path("pdf/<int:pk>/", RenderPDF.as_view(), name="chat-pdf"),
    path("pdf/<int:pk>/delete/", ChatPDFDeleteView.as_view(), name="chat-pdf-delete"),

    path("teachable-agent/", TeachableAgentView.as_view(), name="teachable-agent"),
    path("create-teachable-agent/", CreateTeachableAgent.as_view(), name="create-teachable-agent"),
    path("teachable/<str:slug>/", TeachableView.as_view(), name="teachable"),
    path("test-teachable-agent/", TestTeachableView.as_view(), name="test-teachable-agent"),
    path("teachable-agent/<str:slug>/delete/", TeachableAgentDeleteView.as_view(), name="teachable-agent-delete"),

    path("group-chat/", GroupChatListView.as_view(), name="group-chat"),
    path("create-group-chat/", GroupChatCreateView.as_view(), name="create-group-chat"),
    path("agent/<str:slug>/", AgentView.as_view(), name="agent"),
    path("create-agent/", AgentCreateView.as_view(), name="create-agent"),
    path("agent/<str:slug>/delete/", AgentDeleteView.as_view(), name="agent-delete"),
    path("agent/<str:slug>/update/", AgentUpdateView.as_view(), name="agent-update"),

    path("chat-group/", GroupChatView.as_view(), name="group-chat-view"),
]