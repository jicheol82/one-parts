from django.urls import path
from users import views

app_name = "users"

urlpatterns = [
    path("account/", views.AccountUpdateView.as_view(), name="account"),
    path("update-password", views.UpdatePasswordView.as_view(), name="password"),
]
