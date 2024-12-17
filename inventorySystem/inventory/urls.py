from django.urls import path
from . import views


urlpatterns = [
    path('', views.inventory_list, name='inventory_list'),
    path('per_product/<int:id>', views.per_product_view, name='per_product'),
   
]