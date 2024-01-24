from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm

from .forms import RegisterForm


def register(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        if request.method == "POST":
            form = RegisterForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data["username"]
                email = form.cleaned_data["email"]
                password = form.cleaned_data["password1"]
                user = authenticate(username=username, password=password)
                messages.success(request, "Account created successfully")
                login(request, user)
                return redirect("dashboard")

        else:
            form = RegisterForm()
        return render(request, "pages/accounts/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    else:
        if request.method == "POST":
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, "Logged in successfully")
                return redirect("dashboard")
            else:
                messages.error(request, "Invalid username or password")
        return render(request, "pages/accounts/login.html")


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect("accounts:login")


def reset_password(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Password reset email sent successfully")
            return redirect("accounts:login")
        else:
            messages.error(request, "Invalid email address")
    else:
        form = PasswordResetForm()
    return render(request, "pages/accounts/reset_password.html", {"form": form})