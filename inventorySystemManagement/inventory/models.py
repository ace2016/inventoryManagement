from collections.abc import Iterable
from django.db import models

# Create your models here.
class Product(models.Model):
	# Blank is for form purpose, null is for the SQL database
	product_code = models.CharField(max_length=50, null=False, blank=False, primary_key=True, unique=True)
	name = models.CharField(max_length=100, null=False, blank=False)
	cost_per_item = models.DecimalField(max_digits=19, decimal_places=2, null=False, blank=False)
	quantity_in_stock = models.IntegerField(null=False, blank=False)
	quantity_sold = models.IntegerField(null=False, blank=False)
	sales = models.DecimalField(max_digits=19, decimal_places=2, null=False, blank=False)
	stock_date = models.DateField(auto_now_add=True)
	last_sales_date = models.DateField(auto_now=True)

	def __str__(self) -> str:
		return self.name
	

class Location(models.Model):
	name = models.CharField(max_length=100, null=False, blank=False, primary_key=True)
	date_created = models.DateField(auto_now_add=True)
	date_updated = models.DateField(auto_now=True)

	def __str__(self) -> str:
		return self.name
	
class ProductMovement(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	product_name = models.CharField(max_length=100, null=True, blank=True)
	quantity_moved = models.IntegerField(null=False, blank=False)
	from_location = models.ForeignKey(Location, related_name="from_location", on_delete=models.CASCADE)
	to_location = models.ForeignKey(Location, related_name="to_location", on_delete=models.CASCADE)
	date_created = models.DateField(auto_now_add=True)
	date_moved = models.DateField(auto_now=True)

	def __str__(self) -> str:
		return self.product_name + " " + self.to_location.name
	

	def save(self, *args, **kwargs) -> None:
		self.product_name = self.product.name
		return super(ProductMovement, self).save(*args, **kwargs)
	

