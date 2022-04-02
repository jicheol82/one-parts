from django.contrib import admin
from .models import *


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
        "seller",
        "num_product",
        "new_part",
        "contact_person",
        "contact_number",
        "price",
        "category",
    )
