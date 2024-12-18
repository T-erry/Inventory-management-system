from django.shortcuts import get_object_or_404, render, redirect
from .models import Inventory
from django.contrib.auth.decorators import login_required
from .forms import AddInventoryForm





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
            return redirect("/inventory/")
    else:
        # Create an empty form for GET requests
        add_form = AddInventoryForm()


    return render(request, "inventory/add_inventory.html", {"form": add_form})

@login_required
def delete_inventory(request, id):
    inventory = get_object_or_404(Inventory, pk=id)
    inventory.delete()
    return redirect("/inventory/")




        

