from django.contrib import admin
from virtualpools.models import *


@admin.register(OtherMakerName)
class OtherMakerNameAdmin(admin.ModelAdmin):
    pass


@admin.register(OfficialMakerName)
class OfficialMakerNameAdmin(admin.ModelAdmin):
    filter_horizontal = ("other_names",)


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    search_fields = ("stock_name", "maker__name", "model_name")
    list_display = ("__str__", "total_stock")


@admin.register(StockInfo)
class StockInfoAdmin(admin.ModelAdmin):
    list_filter = ("new_part", "my_stock__maker")
    list_display = (
        "owner",
        "my_stock",
        "num_stock",
        "place",
        "new_part",
        "contact_person",
        "contact_number",
    )
