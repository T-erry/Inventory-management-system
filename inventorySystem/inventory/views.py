from django.shortcuts import get_object_or_404, render, redirect
from .models import Inventory
from django.contrib.auth.decorators import login_required
from .forms import AddInventoryForm, UpdateInventoryForm
from django.contrib import messages





# Create your views here.
@login_required
def inventory_list(request):
    inventories = Inventory.objects.all()
    context ={
        "title" : "Inventory list",
        "inventories": inventories

    }
    return render(request, "inventory/inventory_list.html", context=context)


@login_required
def per_product_view(request, id):
    inventory = get_object_or_404(Inventory, pk=id)
    context = {
        'inventory': inventory,
    }

    return render(request, "inventory/per_product.html", context=context)


@login_required
def add_inventory(request):
    if request.method == "POST":
        # Populate the form with POST data
        add_form = AddInventoryForm(data=request.POST)  
        # Check if all fields are valid
        if add_form.is_valid():
            # Create an unsaved instance
            new_inventory = add_form.save(commit=False)
            # Calculate the total sales
            new_inventory.sales = float(add_form.cleaned_data['cost_per_item']) * float(add_form.cleaned_data['quantity_sold'])
            new_inventory.save()
            messages.success(request, "Successfully Added Inventory" )
            return redirect("/inventory/")
    else:
        # Create an empty form for GET requests
        add_form = AddInventoryForm()


    return render(request, "inventory/add_inventory.html", {"form": add_form})

@login_required
def delete_inventory(request, id):
    inventory = get_object_or_404(Inventory, pk=id)
    inventory.delete()
    messages.error(request, "Inventory Deleted")
    return redirect("/inventory/")

@login_required
def update_inventory(request, id):
    inventory = get_object_or_404(Inventory, pk=id)
    
    if request.method == 'POST':
        update_form = UpdateInventoryForm(data=request.POST)
        if update_form.is_valid():
            inventory.name = update_form.cleaned_data['name']
            inventory.cost_per_item = update_form.cleaned_data['cost_per_item']
            inventory.quantity_in_stock = update_form.cleaned_data['quantity_in_stock']
            inventory.quantity_sold = update_form.cleaned_data['quantity_sold']
            inventory.sales = float(update_form.cleaned_data['cost_per_item']) * float(update_form.cleaned_data['quantity_sold'])
            inventory.save()
            messages.success(request, "Inventory Updated")
            return redirect(f"/inventory/per_product/{id}")
    else:
         # Initialize form with inventory data for GET request
        update_form = UpdateInventoryForm(instance=inventory) 

    context = {"form": update_form}
    return render(request, "inventory/update_inventory.html", context=context)

