from django.contrib import admin
from django.utils.html import mark_safe
from .models import *


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):

    """Phot Admin Definition"""

    list_display = ("__str__", "get_thumbnail")

    def get_thumbnail(self, obj):
        return mark_safe(f'<img width="50px" src="{obj.file.url}" />')

    get_thumbnail.short_description = "Thumbnail"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = (
        "product_name",
        "maker__name",
        "model_name",
        "seller__username",
        "category__name",
    )
    list_filter = (
        "seller__my_company",
        "category",
    )
    list_display = (
        "__str__",
        "seller_name",
        "num_product",
        "new_part",
        "price",
        "category",
    )
