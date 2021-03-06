from django.urls import path
from core import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.log_out, name="logout"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path(
        "verify/<str:key>/",
        views.complete_verification,
        name="complete_verification",
    ),
    path("service/<str:service>", views.service_exp),
]
