from django.urls import path
from . import views


urlpatterns = [
    path('', views.inventory_list, name='inventory_list'),# Admin only
    path('per_product/<int:id>', views.per_product_view, name='per_product'),
    path('add_inventory/', views.add_inventory, name='add_inventory'),
    path('delete/<int:id>', views.delete_inventory, name='delete_inventory'),
    path('update/<int:id>', views.update_inventory, name='update_inventory'),
    path('signup/', views.sign_up, name='signup'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('password_change', views.password_change, name='password_change'),
    path('password_reset', views.password_reset, name='password_reset'),
    path('reset/<uidb64>/<token>', views.passwordResetConfirm, name='password_reset_confirm'),
    path('dashboard/', views.dashboard, name='dashboard'),
   

  
   
]
   
