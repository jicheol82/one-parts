from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView
from core.forms import *


def home(request):
    # 아마 여기서 로그인 체크를 해야겠지?

    return render(request, "home/home.html")


class LoginView(FormView):
    form_class = LoginForm
    template_name = "home/login.html"
