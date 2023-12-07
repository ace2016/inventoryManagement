from django.urls import path
from inventory.views import *

#URL Routes
urlpatterns = [
    path("", index, name="products"),
	path("single_product/<pk>", single_product, name="single_product"),
	path("product_add/", add_product, name="product_add"),
	path("delete/<pk>", delete_inventory, name="delete_inventory"),
	path("update/<pk>", update_inventory, name="update_inventory"),
	path("location_add/", add_location, name="location_add"),
	
]