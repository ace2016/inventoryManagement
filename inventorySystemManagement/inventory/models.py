from collections.abc import Iterable
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


CHOICES = (
	('Stock Receipt', 'Stock Receipt'),
	('Stock Transfer', 'Stock Transfer'),
	('Stock Issue', 'Stock Issue')
)

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
	# balance = models.DecimalField(max_digits=19, decimal_places=2, null=False, blank=False, default=0)

	def __str__(self) -> str:
		return self.name
	

class Location(models.Model):
	name = models.CharField(max_length=100, null=False, blank=False, primary_key=True)
	date_created = models.DateField(auto_now_add=True)
	date_updated = models.DateField(auto_now=True)

	def __str__(self) -> str:
		return self.name
	
	
class ProductMovement(models.Model):
	transaction_type = models.CharField(max_length=15, choices=CHOICES, default="Stock Receipt")
	date_created = models.DateField(auto_now_add=True)
	date_moved = models.DateField(auto_now=True)

	def __str__(self) -> str:
		return str(self.id) # self.product_name + " " + self.to_location.name
	
	def save(self, *args, **kwargs) -> None:
		# self.product_name = self.product.name
		return super(ProductMovement, self).save(*args, **kwargs)
	
class ProductMovementItem(models.Model):
	product_movement = models.ForeignKey(ProductMovement, related_name='movement_items', on_delete=models.CASCADE)
	product = models.ForeignKey(Product, related_name='movement_product', on_delete=models.CASCADE)
	product_name = models.CharField(max_length=100, null=True, blank=True)
	quantity = models.IntegerField(null=False, blank=False)
	from_location = models.ForeignKey(Location, related_name="from_location", null=True, blank=True, on_delete=models.CASCADE)
	to_location = models.ForeignKey(Location, related_name="to_location", null=True, blank=True, on_delete=models.CASCADE)

	def __str__(self):
		return '{}'.format(self.id)
	
	def save(self, *args, **kwargs) -> None:
		self.product_name = self.product.name
		return super(ProductMovementItem, self).save(*args, **kwargs)
	

class MovementLedger(models.Model):
	product_movement = models.ForeignKey(ProductMovement, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	product_name = models.CharField(max_length=100, null=True, blank=True)
	transaction_type = models.CharField(max_length=15, choices=CHOICES, default="Stock Receipt")
	quantity = models.IntegerField(null=False, blank=False)
	from_location = models.ForeignKey(Location, related_name="from_location_ledger", 
		null=True, blank=True, on_delete=models.CASCADE)
	to_location = models.ForeignKey(Location, related_name="to_location_ledger", 
		null=True, blank=True, on_delete=models.CASCADE)	
	# balance_before_movement = models.DecimalField(null=False, blank=False, 
	# 	decimal_places=2, max_digits=10)
	# balance_after_movement = models.DecimalField(null=False, blank=False, 
	# 	decimal_places=2, max_digits=10)
	date_created = models.DateField(auto_now_add=True)
	date_moved = models.DateField(auto_now=True)

	def __str__(self) -> str:
		return self.product_name
	
	def save(self, *args, **kwargs) -> None:
		self.product_name = self.product.name
		return super(MovementLedger, self).save(*args, **kwargs)




@receiver(post_save, sender=ProductMovementItem)
def save_profile(sender, instance, **kwargs):
# 	"""
# 		To get balance_before_movement
# 		subtract quantity from stock balance if balance - qty > 0

# 	"""
	from_location = ""
	to_location = ""
	balance_before_movement = 0
	balance_after_movement = 0

	if instance.product_movement.transaction_type == "Stock Reciept":
		to_location = instance.to_location
	elif instance.product_movement.transaction_type == "Stock Transfer":
		to_location = instance.to_location
		from_location = instance.from_location
	else:
		from_location = instance.from_location
	
# 	# set balance
# 	# balance_after_movement = instance.product.balance + instance.quantity

	movement_ledger = MovementLedger.objects.create(
		product_movement = instance.product_movement,
		product = instance.product,
		transaction_type = instance.product_movement.transaction_type,
		quantity = instance.quantity,
		from_location = instance.from_location,
		to_location = instance.to_location,
	)