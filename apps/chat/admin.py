from django.contrib import admin

from .models import Chat, PDF, TeachableAgent


admin.site.register(PDF)
admin.site.register(TeachableAgent)