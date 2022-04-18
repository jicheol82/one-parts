from django.contrib import admin
from .models import *


@admin.register(Feed)
class FeedAdmin(admin.ModelAdmin):
    search_fields = (
        "writer",
        "content",
    )
    list_display = ("__str__", "count_reply")


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    search_fields = (
        "writer",
        "content",
    )
    list_display = ("__str__", "original_feed")
