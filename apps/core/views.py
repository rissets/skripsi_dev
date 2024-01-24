from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render

from django.views import View


class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "pages/home.html", {})

    def post(self, request):
        return HttpResponse("OK")

