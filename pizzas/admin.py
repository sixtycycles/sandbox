from django.contrib import admin

from .models import DeliveryLabel, Item, Order, Vendor


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "state", "email", "phone")
    search_fields = ("name", "city", "email")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "vendor", "timestamp_created")
    list_filter = ("vendor",)
    search_fields = ("user__username", "vendor__name")


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order",
        "unit",
        "quantity",
        "cost_per_unit",
        "catalog_number",
    )
    search_fields = ("unit", "catalog_number", "description")


@admin.register(DeliveryLabel)
class DeliveryLabelAdmin(admin.ModelAdmin):
    list_display = ("deliver_to", "email", "room_number", "ship_method", "mark_urgent")
    search_fields = ("deliver_to", "order_contact_name")
