from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# 설비 Admin
@admin.register(EquipGroup)
class EuipGroupAdmin(admin.ModelAdmin):
    """EuipGroup Admin"""

    search_fields = ("name",)
    list_display = ("name", "count_equips")

    def count_equips(self, obj):
        return obj.equipment_set.count()

    count_equips.short_description = "#Equipments"


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    """Equipment Admin"""

    search_fields = ("name",)
    list_display = ("name", "group")
    list_filter = ("group__name",)
    raw_id_fields = ("group",)


# 회사 Admin
@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    """Domain Admin Definition"""

    search_fields = ("name", "company__name")
    list_display = ("name", "company")
    raw_id_fields = ("company",)


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    """Domain Admin Definition"""

    # list_display = ("name",)
    pass


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    """Company Admin Definition"""

    search_fields = ("name",)

    list_display = (
        "name",
        "count_domains",
        "count_members",
        "count_branches",
        "created",
        "updated",
    )

    # make "MtoM select form" beautiful
    filter_horizontal = ("branches",)

    def count_domains(self, obj):
        return obj.domain_set.count()

    count_domains.short_description = "#Domains"

    def count_members(self, obj):
        return obj.user_set.count()

    count_members.short_description = "#Members"

    def count_branches(self, obj):
        return obj.branches.count()

    count_branches.short_description = "#Branches"


# User Admin
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Custom User Admin"""

    search_fields = (
        "username",
        "email",
        "company",
    )
    list_filter = (
        "is_verified",
        "is_active",
        "company",
    )

    # overal view
    list_display = (
        "username",
        "profile_img",
        "email",
        "company",
        "branch",
        "count_equips",
        "is_verified",
        "is_superuser",
        "is_active",
        "last_login",
    )

    # detail view
    fieldsets = (
        (
            "Custom Profile",
            {
                "fields": (
                    "profile_img",
                    "username",
                    "email",
                    "company",
                    "branch",
                    "my_equips",
                    "is_verified",
                    "token",
                    "is_staff",
                    "is_active",
                    "date_joined",
                )
            },
        ),
    )

    raw_id_fields = ("company", "branch")
    filter_horizontal = ("my_equips",)

    def count_equips(self, obj):
        return obj.my_equips.count()

    count_equips.short_description = "#equips"
