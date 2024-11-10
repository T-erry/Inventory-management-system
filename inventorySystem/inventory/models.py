from django.db import models

# Create your models here.
class Inventory(models.Model):
    name = models.charField(max_length=100, null=False, blank=False)
    cost_per_item = models.DecimalField(max_digits=19, decimal_places=2, null=False, blank=False)
    quantity_in_stock = models.IntegerField(null=False)

