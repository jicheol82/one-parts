from django.urls import path
from virtualpools import views

app_name = "virtualpools"

urlpatterns = [
    path("", views.VirtualPoolView.as_view(), name="virtualpool"),
    path("<int:pk>/", views.virtualpoolDetailView, name="detail"),
    path("register", views.virtualPoolCreateView, name="create"),
    path("<int:pk>/edit", views.VirutalPoolEditView.as_view(), name="edit"),
    path("<int:pk>/delete", views.virtualPoolDeleteView, name="delete"),
]
