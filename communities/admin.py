from django.contrib import admin
from .models import *


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    pass


@admin.register(Feed)
class FeedAdmin(admin.ModelAdmin):
    list_display = ("__str__", "writer", "count_reply", "created", "updated")
