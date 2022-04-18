from django.contrib import admin
from django.utils.html import mark_safe
from .models import *


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    """Phot Admin Definition"""

    list_display = ("__str__", "get_thumbnail")
    # 썸네일 화면을 리스트에 보여준다
    def get_thumbnail(self, obj):
        return mark_safe(f'<img width="50px" src="{obj.file.url}" />')

    get_thumbnail.short_description = "Thumbnail"


# 사진 추가 창 모양
class PhotoInline(admin.TabularInline):
    model = Photo


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = (
        "name",
        "seller",
        "maker",
        "model_name",
        "spec",
        "description",
    )
    list_filter = (
        "is_new",
        "on_sale",
        "category",
    )
    list_display = (
        "name",
        "maker",
        "is_new",
        "num_product",
        "price",
        "category",
        "seller",
    )
    inlines = (PhotoInline,)
    raw_id_fields = (
        "seller",
        "maker",
        "category",
    )
