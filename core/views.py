from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import FormView
from core.forms import *


def home(request):
    # 정적인 페이지를 보여준다
    return render(request, "home/home.html")


class LoginView(FormView):
    form_class = LoginForm
    template_name = "home/login.html"
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))
