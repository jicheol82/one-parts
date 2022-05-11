from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import FormView
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from core.forms import *
from core.mixins import OnlyForGuest
from users.models import User


def home(request):
    # 정적인 페이지를 보여준다
    return render(request, "home/home.html")


class LoginView(OnlyForGuest, FormView):
    form_class = LoginForm
    template_name = "home/login.html"

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        next_url = self.request.GET.get("next")
        if next_url is not None:
            return next_url
        else:
            return reverse("core:home")


# @user_passes_test(lambda u: u.is_authenticated, login_url="core:home")
def log_out(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("core:home")


class SignUpView(OnlyForGuest, FormView):
    form_class = SignUpForm
    template_name = "home/signup.html"
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=username, password=password)
        messages.success(self.request, "Success to join, please verify your email.")
        user.verify_email()
        return super().form_valid(form)


def complete_verification(request, key):
    try:
        user = User.objects.get(token=key)
        user.is_verified = True
        user.token = ""
        user.save()
        messages.success(request, "You are verified! Please log in")
    except User.DoesNotExist:
        messages.error(request, "You are not verified safely")
    return redirect(reverse("core:home"))


def service_exp(request, service):
    if service == "virtualpool":
        return render(request, "home/virtualpool.html")
    elif service == "partsmarket":
        return render(request, "home/partsmarket.html")
    elif service == "community":
        return render(request, "home/community.html")
    else:
        return None
