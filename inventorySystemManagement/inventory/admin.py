from django.contrib import admin
from inventory.models import (
    Location, Product, ProductMovement, ProductMovementItem,
    MovementLedger,
)

# Register your models here.
admin.site.register(Location)
# admin.site.register(ProductMovement)
admin.site.register(MovementLedger)


@admin.register(Product) #decorator
class ProductAdmin(admin.ModelAdmin):
    list_display = ["product_code", "name", "cost_per_item"]
    search_fields = ["product_code", "name"] 
    ordering = ["stock_date"]
    # readonly_fields=["product_code"]

class ProductMovementItemInline(admin.TabularInline):
    model = ProductMovementItem
    raw_id_fields = ['product']

@admin.register(ProductMovement)
class ProductMovementAdmin(admin.ModelAdmin):
    list_display = ["pk", "transaction_type", "date_created",]
    search_fields = ["pk", "transaction_type", "date_created"] 
    ordering = ["-date_created"]
    inlines = [ProductMovementItemInline]
    # readonly_fields=["product_code"]