from django.contrib import admin
from virtualpools.models import *


@admin.register(OtherMakerName)
class OtherMakerNameAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "official_name",
    )
    list_filter = ("official_name",)


@admin.register(OfficialMakerName)
class OfficialMakerNameAdmin(admin.ModelAdmin):
    pass


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    search_fields = ("stock_name", "model_name")
    list_display = ("__str__", "total_stock")
    list_filter = ("maker__name",)


@admin.register(StockInfo)
class StockInfoAdmin(admin.ModelAdmin):
    list_filter = (
        "owner__my_company__name",
        "my_stock__maker",
        "new_part",
    )
    list_display = (
        "owner",
        "my_stock",
        "num_stock",
        "place",
        "new_part",
        "contact_person",
        "contact_number",
    )
    raw_id_fields = ("my_stock", "owner")
