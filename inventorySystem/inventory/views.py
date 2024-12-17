from django.shortcuts import get_object_or_404, render
from .models import Inventory
from django.contrib.auth.decorators import login_required





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
