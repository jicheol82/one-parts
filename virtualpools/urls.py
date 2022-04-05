from django.urls import path
from virtualpools import views

app_name = "virtualpools"

urlpatterns = [path("", views.VirtualPoolView.as_view(), name="virtualpools")]
