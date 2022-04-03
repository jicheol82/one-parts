from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# 설비 Admin
@admin.register(EquipGroup)
class EuipGroupAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("name", "count_equips")

    def count_equips(self, obj):
        return obj.equipment_set.count()

    count_equips.short_description = "#Equipments"


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("name", "equipment_group")
    list_filter = ("equipment_group",)
    raw_id_fields = ("equipment_group",)


# 회사 Admin
@admin.register(Domain, Branch)
class DomainAdmin(admin.ModelAdmin):
    """Domain Admin Definition"""

    list_display = ("name",)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    """Company Admin Definition"""

    search_fields = ("name", "domains", "branches")

    list_display = (
        "name",
        "count_domains",
        "count_members",
        "count_branches",
        "created",
        "updated",
    )

    # make "MtoM select form" beautiful
    filter_horizontal = ("domains", "branches")

    def count_domains(self, obj):
        return obj.domains.count()

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
        "nickname",
        "my_company__name",
        "company_email",
        "contact_number",
    )
    list_filter = (
        "my_company",
        "interesting_equips",
    ) + UserAdmin.list_filter

    # overal view
    list_display = (
        "username",
        "nickname",
        "count_equips",
        "my_company",
        "my_branch",
        "company_email",
        "contact_number",
        "is_active",
        "is_staff",
        "is_superuser",
        "date_joined",
        # "email_verified",
        # "email_secret",
        # "login_method",
    )

    raw_id_fields = ("my_company", "my_branch")

    def count_equips(self, obj):
        return obj.interesting_equips.count()

    count_equips.short_description = "#equips"

    # detail view
    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom Profile",
            {
                "fields": (
                    "profile_img",
                    "nickname",
                    "my_company",
                    "company_email",
                    "contact_number",
                    "interesting_equips",
                )
            },
        ),
    )

    filter_horizontal = ("interesting_equips",)
