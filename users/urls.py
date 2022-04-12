from django.urls import path
from users import views

app_name = "users"

urlpatterns = [
    path("<int:pk>/", views.ProfileView.as_view(), name="profile"),
    path(
        "update-profile/", views.UserUpdateProfileView.as_view(), name="update-profile"
    ),
    path("update-password", views.UpdatePasswordView.as_view(), name="password"),
]
