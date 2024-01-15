from django.contrib import admin
from .models import Warehouse, WarehouseType

@admin.register(WarehouseType)
class wareHouseTypeAdmin(admin.ModelAdmin):
    list_display=['id','warehouse_type_title']


@admin.register(Warehouse)
class wareHouseAdmin(admin.ModelAdmin):
    list_display=['product','user_registered','price','qty','warehouse_type','register_date']

