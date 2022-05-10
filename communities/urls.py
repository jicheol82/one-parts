from django.urls import path
from communities import views

app_name = "communities"

urlpatterns = [
    path("", views.FeedListView.as_view(), name="feed"),
    path("write/", views.FeedCreateView.as_view(), name="write"),
    path("<int:pk>/", views.FeedDetailView.as_view(), name="feed_detail"),
    path("<int:pk>/edit", views.FeedUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete", views.feedDelete, name="delete"),
    path("<int:pk>/reply", views.replyCreateView, name="reply_create"),
    path("<int:pk>/reply/<int:r_pk>", views.replyDeleteView, name="reply_delete"),
]
