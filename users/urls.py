from django.urls import path
from users import views

app_name = "users"

urlpatterns = [
    path("account/", views.AccountView.as_view(), name="account"),
    path(
        "update-profile/", views.UserUpdateProfileView.as_view(), name="update-profile"
    ),
    path("update-password", views.UpdatePasswordView.as_view(), name="password"),
]
