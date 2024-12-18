from django.urls import path
from . import views


urlpatterns = [
    path('', views.inventory_list, name='inventory_list'),
    path('per_product/<int:id>', views.per_product_view, name='per_product'),
    path('add_inventory/', views.add_inventory, name='add_inventory'),
    path('delete/<int:id>', views.delete_inventory, name='delete_inventory'),
     path('update/<int:id>', views.update_inventory, name='update_inventory'),
   
]
   
