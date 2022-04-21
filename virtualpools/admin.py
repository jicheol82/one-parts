from django.contrib import admin
from virtualpools.models import *


@admin.register(OldMakerName)
class OldMakerNameAdmin(admin.ModelAdmin):
    """Old Maker Name Admin"""

    search_fields = ("name", "official_name")
    list_display = (
        "name",
        "official_name",
    )
    list_filter = ("official_name",)


@admin.register(OfficialMakerName)
class OfficialMakerNameAdmin(admin.ModelAdmin):
    """Official Maker Name Admin"""

    pass


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    """Stock Information Admin"""

    search_fields = ("name", "maker__name", "model_name")
    list_display = ("name", "maker", "model_name", "total_stock")
    list_filter = ("maker__name",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "maker",
                    "model_name",
                    "spec",
                ),
            },
        ),
    )


@admin.register(StockInfo)
class StockInfoAdmin(admin.ModelAdmin):
    search_fields = (
        "owner__username",
        "my_stock__name",
        "my_stock__maker__name",
        "my_stock__model_name",
        "place",
        "contact_person",
        "contact_info",
    )
    list_filter = (
        "is_new",
        "my_stock__maker",
    )
    list_display = (
        "owner",
        "my_stock",
        "num_stock",
        # "my_stock__total_stock",
        "is_new",
        "contact_person",
        "contact_info",
    )
    raw_id_fields = (
        "owner",
        "my_stock",
    )
