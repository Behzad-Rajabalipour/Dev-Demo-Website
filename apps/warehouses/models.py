from django.db import models
from apps.products.models import Product
from apps.accounts.models import CustomUser

class WarehouseType(models.Model):
    warehouse_type_title=models.CharField(max_length=50, verbose_name="warehouse type")
    
    def __str__(self):
        return self.warehouse_type_title
    
    class Meta:
        verbose_name= "warehouse type"
        verbose_name_plural= "warehouses type"

#----------------------------------------------------------------------
class Warehouse(models.Model):
    warehouse_type=models.ForeignKey(WarehouseType, on_delete=models.CASCADE, related_name="warehouses")
    user_registered=models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user_warehouses")
    product=models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_warehouses")
    qty=models.IntegerField()
    price=models.IntegerField(null=True, blank=True)
    register_date=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.warehouse_type} - {self.product}"
    
    class Meta:
        verbose_name= "warehouse"
        verbose_name_plural= "warehouses"
