from django.contrib import admin
from inventory.models import *

# Register your models here.
admin.site.register(Location)
admin.site.register(ProductMovement)


@admin.register(Product) #decorator
class ProductAdmin(admin.ModelAdmin):
    list_display = ["product_code", "name", "cost_per_item"]
    search_fields = ["product_code", "name"] 
    ordering = ["stock_date"]
    # readonly_fields=["product_code"]