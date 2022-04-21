from django.urls import path
from communities import views

app_name = "communities"

urlpatterns = [
    path("", views.FeedView.as_view(), name="feed"),
    path("<int:pk>/", views.ReplyView.as_view(), name="reply"),
]
