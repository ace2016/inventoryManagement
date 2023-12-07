from django.forms import ModelForm
from inventory.models import *

#Form to Add Products to the DB - scal
class AddProductForm(ModelForm):
	class Meta:
		model = Product
		fields = ['product_code', 'name', 'cost_per_item', 'quantity_in_stock', 'quantity_sold']

class UpdateProductForm(ModelForm):
	class Meta:
		model = Product
		fields = ['name', 'cost_per_item', 'quantity_in_stock', 'quantity_sold']

class AddLocationForm(ModelForm):
	class Meta:
		model = Location
		fields = ['name']