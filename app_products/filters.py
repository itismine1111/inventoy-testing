from django_filters import rest_framework as filters
from .models import Inventory
import django_filters


class InventoryFilter(filters.FilterSet):

    name = django_filters.CharFilter(
        label="Name", field_name="ItemName", lookup_expr="startswith"
    )

    class Meta:
        model = Inventory
        fields = ["name", "Group__id", "Location__id", "Category__id", "ItemStatus", "Supplier__id"]
