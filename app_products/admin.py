from django.contrib import admin
from .models import Group, Location, Category, Inventory, InventoryStockTransaction, InventorySDSRecord, Supplier, UnitsMeasure


admin.site.register(Group)
admin.site.register(Location)
admin.site.register(Category)
# admin.site.register(Status)
admin.site.register(Inventory)
admin.site.register(InventoryStockTransaction)
admin.site.register(InventorySDSRecord)
admin.site.register(Supplier)
admin.site.register(UnitsMeasure)
