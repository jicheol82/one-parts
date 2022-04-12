from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import FormView
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
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
            messages.success(self.request, f"Welcome back {user.nickname}")
        return super().form_valid(form)

    def get_success_url(self):
        next_url = self.request.GET.get("next")
        if next_url is not None:
            return next_url
        else:
            return reverse("core:home")


def log_out(request):
    messages.success(request, "See you later")
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(OnlyForGuest, FormView):
    form_class = SignUpForm
    template_name = "home/signup.html"
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=username, password=password)
        user.veryfy_email()
        return super().form_valid(form)

    # initial = {'필드명':"필드값",}


def complete_verification(request, opt, key):
    try:
        if opt == "user":
            user = User.objects.get(user_secret=key)
            user.user_verified = True
            user.user_secret = ""
        elif opt == "company":
            user = User.objects.get(company_secret=key)
            user.company_verified = True
            user.company_secret = ""
        else:
            print("abnormal access")
    except User.DoesNotExist:
        # to do : error message
        pass
    user.save()
    return redirect(reverse("core:home"))
