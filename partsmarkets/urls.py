from django.urls import path
from partsmarkets import views

app_name = "partsmarkets"

urlpatterns = [
    path("", views.PartsMarketView.as_view(), name="partsmarket"),
    path("<int:pk>", views.DetailView.as_view(), name="detail"),
]
