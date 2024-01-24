from django.contrib import admin

from .models import Chat, PDF, TeachableAgent, GroupChat, Agent


admin.site.register(PDF)
admin.site.register(TeachableAgent)
admin.site.register(GroupChat)
admin.site.register(Agent)
