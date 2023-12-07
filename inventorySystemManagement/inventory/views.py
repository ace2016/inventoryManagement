from django.shortcuts import redirect, render, get_object_or_404
from inventory.models import *
from django.contrib.auth.decorators import login_required
from inventory.forms import *
from django.contrib import messages

# Create your views here.
# Product/Location list views
@login_required
def index(request):
	inventories = Product.objects.all()
	locations = Location.objects.all()
	context = {
		"title": "Dashboard",
		"inventories": inventories,
		"locations": locations
	}
	return render(request, "inventory_files/product.html", context=context)

# Single List product view
@login_required
def single_product(request, pk):
	inventory = get_object_or_404(Product, pk=pk)
	context = {
		"title": "Single Product Page",
		"inventory": inventory
	}
	return render(request, "inventory_files/single_product.html", context=context)

# Adding Products to DB
@login_required
def add_product(request):
	if request.method == "POST":
		add_form = AddProductForm(data=request.POST)
		if add_form.is_valid():
			new_inventory = add_form.save(commit=False)
			new_inventory.sales = float(add_form.data['cost_per_item']) * float(add_form.data['quantity_sold'])
			new_inventory.save()
			messages.success(request, "Successfully Added Product")
			return redirect("/inventory/")
	else:
		add_form = AddProductForm()
	context = {"form": add_form, "title": "Add Product"}
	return render(request, "inventory_files/product_add.html", context=context)


#Deleting Products to DB
@login_required
def delete_inventory(request, pk):
	if Product.objects.filter(pk=pk):
		Product.objects.get(pk=pk).delete()
	return redirect("/inventory/")

#Updating Products to DB
@login_required
def update_inventory(request, pk):
	inventory = get_object_or_404(Product, pk=pk)
	if request.method == "POST":
		updateForm = UpdateProductForm(data=request.POST)
		if updateForm.is_valid():
			inventory.name = updateForm.data['name']
			inventory.cost_per_item = updateForm.data['cost_per_item']
			inventory.quantity_in_stock = updateForm.data['quantity_in_stock']
			inventory.quantity_sold = updateForm.data['quantity_sold']
			inventory.sales = float(inventory.cost_per_item) * float(inventory.quantity_sold)
			inventory.save()
			return redirect(f"/inventory/single_product/{pk}")
	else:
		updateForm = UpdateProductForm(instance=inventory)
	context = {"form": updateForm, "title": "Update Product"}
	return render(request, "inventory_files/product_update.html", context=context)
			
# Adding Location to DB
@login_required
def add_location(request):
	if request.method == "POST":
		location_form = AddLocationForm(data=request.POST)
		if location_form.is_valid():
			new_inventory = location_form.save()
			new_inventory.save()
			return redirect("/inventory/")
	else:
		location_form = AddLocationForm()
	context = {"form": location_form, "title": "Add Location"}
	return render(request, "inventory_files/add_location.html", context=context)