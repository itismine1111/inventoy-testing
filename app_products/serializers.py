from importlib.metadata import requires
from typing_extensions import Required
from webbrowser import get
from django.utils.timezone import localdate
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
import base64
import json

from rest_framework import serializers

from drf_extra_fields.fields import HybridImageField

from app_account.serializers import UserSerializer

from .models import (
    Inventory,
    Group,
    Category,
    InventoryStockTransaction,
    Location,
    Supplier,
    InventorySDSRecord,
    UnitsMeasure,
)

from app_account.serializers import UserSerializer


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class StatusSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=1)
    name = serializers.CharField(max_length=20)


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = "__all__"


class UnitsMeasureSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitsMeasure
        fields = "__all__"


class InventorySDSRecordSerializer(serializers.ModelSerializer):
    SDSComponent = serializers.CharField(
        required=False, allow_blank=True, allow_null=True
    )
    SDSCasNo = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    # Barcode = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    # SDSNameURL = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    # SDSOnFile = serializers.BooleanField(required=False, allow_null=True)

    class Meta:
        model = InventorySDSRecord
        fields = (
            "id",
            "SDSCasNo",
            "SDSComponent",
            "SDSLocationURL",
            "SDSNameURL",
            "SDSOnFile",
            "IDRecord",
        )

    def create(self, validated_data):
        request = self.context.get("request")

        obj = InventorySDSRecord.objects.create(**validated_data)  # saving post object
        obj.DateEntered = localdate()
        obj.idSDS = obj.id
        obj.save()
        return obj


class InventoryStockTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryStockTransaction
        fields = "__all__"


class InventorySerializer(serializers.ModelSerializer):
    Group = GroupSerializer(many=True)
    Location = LocationSerializer(many=True)
    Category = CategorySerializer(many=True)
    Supplier = SupplierSerializer(many=True)
    SDSRecords = serializers.SerializerMethodField("get_sds_records_for_product")
    StockTransactions = serializers.SerializerMethodField(
        "get_stock_transactions_for_product"
    )
    UnitsMeasure = UnitsMeasureSerializer()
    stock_availability_value = serializers.SerializerMethodField(
        "get_stock_availability_value"
    )
    tax_amt_value = serializers.SerializerMethodField("get_tax_amt_value")
    units_on_hand_value = serializers.SerializerMethodField("get_units_on_hand_value")
    stock_ext_value = serializers.SerializerMethodField("get_stock_ext_value")
    RequestedBy = UserSerializer()
    RequestApprovedBy = UserSerializer()

    class Meta:
        model = Inventory
        fields = "__all__"

    def get_units_on_hand(self, id):
        units_on_hand = 0
        inventory_st = InventoryStockTransaction.objects.filter(IDRecord=id)
        if inventory_st is None or len(inventory_st) == 0:
            return units_on_hand

        for i in inventory_st:
            if i.Units is not None:
                if i.Type == "In":
                    units_on_hand = units_on_hand + i.Units
                else:
                    units_on_hand = units_on_hand - i.Units

        return units_on_hand

    def get_stock_availability_value(self, obj):
        units_on_hand = self.get_units_on_hand(obj.id)

        if obj.ReorderLevel is None or obj.ReorderLevel == "":
            return "Stop | rgb(235,64,36)"

        if obj.ReorderLevel < units_on_hand:
            return "In-Stock | rgb(0,169,0)"

        elif obj.ReorderLevel >= units_on_hand:
            return "Re-order Stock | rgb(255,192,55)"

        elif (obj.ReorderLevel + units_on_hand == 0) or (units_on_hand <= 0):
            return "Stop | rgb(235,64,36)"

        return ""

    def get_units_on_hand_value(self, obj):
        return self.get_units_on_hand(obj.id)

    def get_stock_ext_value(self, obj):
        units_on_hand = self.get_units_on_hand(obj.id)
        if obj.StockUnitPrice is None:
            return 0
        return units_on_hand * obj.StockUnitPrice

    def get_tax_amt_value(self, obj):
        units_on_hand = self.get_units_on_hand(obj.id)
        if obj.StockUnitPrice is not None and obj.TaxRate is not None:
            stock_ext_value = units_on_hand * obj.StockUnitPrice
            return stock_ext_value * obj.TaxRate

        return 0

    def get_sds_records_for_product(self, obj):
        sds_record_objs = InventorySDSRecord.objects.filter(IDRecord=obj.id)
        if sds_record_objs is None or len(sds_record_objs) == 0:
            return {"count": 0, "list": []}

        serializer = InventorySDSRecordSerializer(sds_record_objs, many=True)
        return {"count": len(serializer.data), "list": serializer.data}

    def get_stock_transactions_for_product(self, obj):
        stock_trasanctions_objs = InventoryStockTransaction.objects.filter(
            IDRecord=obj.id
        )
        if stock_trasanctions_objs is None or len(stock_trasanctions_objs) == 0:
            return {"count": 0, "list": []}

        serializer = InventoryStockTransactionSerializer(
            stock_trasanctions_objs, many=True
        )
        return {"count": len(serializer.data), "list": serializer.data}


class CreateInventorySerializer(serializers.ModelSerializer):
    Image = HybridImageField(required=False, allow_null=True)  # From DRF Extra Fields
    SDSLocationURL = serializers.CharField(required=False)
    SDSNameURL = serializers.CharField(required=False)
    ItemDescription = serializers.CharField(
        required=False, allow_null=True, allow_blank=True
    )
    ItemKnownAs = serializers.CharField(
        required=False, allow_null=True, allow_blank=True
    )
    LotNumber = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    DateEntered = serializers.DateTimeField(required=False, allow_null=True)
    ItemKnownAs = serializers.CharField(
        required=False, allow_null=True, allow_blank=True
    )
    DateLastOrdered = serializers.DateTimeField(required=False, allow_null=True)
    DateLastUsed = serializers.DateTimeField(required=False, allow_null=True)
    ModelYear = serializers.IntegerField(required=False, allow_null=True)
    PartNumber = serializers.CharField(
        required=False, allow_null=True, allow_blank=True
    )
    BarCode = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    DateLastReceived = serializers.DateTimeField(required=False, allow_null=True)
    LotNumber = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    SDSOnFile = serializers.BooleanField(default=False, required=False, allow_null=True)
    SDSNameURL = serializers.CharField(
        required=False, allow_null=True, allow_blank=True
    )
    SDSLocationURL = serializers.CharField(
        required=False, allow_null=True, allow_blank=True
    )
    DateModified = serializers.DateTimeField(required=False, allow_null=True)
    ReorderLevel = serializers.FloatField(required=False, allow_null=True)
    MinimumOrder = serializers.FloatField(required=False, allow_null=True)
    StockUnitPrice = serializers.FloatField(required=False, allow_null=True)
    RequestedBy = serializers.EmailField(required=False, allow_null=True)
    RequestedByDate = serializers.DateTimeField(required=False, allow_null=True)
    RequestApprovedBy = serializers.EmailField(required=False, allow_null=True)
    RequestApprovedDate = serializers.DateTimeField(required=False, allow_null=True)
    # groups = GroupSerializer(many=True)
    # locations = LocationSerializer(many=True)
    # categories = CategorySerializer(many=True)
    # suppliers = SupplierSerializer(many=True)

    class Meta:
        model = Inventory
        fields = (
            "DateEntered",
            "RequestedBy",
            "RequestedByDate",
            "ItemName",
            "ItemKnownAs",
            "ItemDescription",
            # "Location",
            # "Category",
            # "Group",
            # "Supplier",
            # "locations",
            # "groups",
            # "categories",
            # "suppliers",
            "ItemStatus",
            "DateLastOrdered",
            "DateLastUsed",
            "ModelYear",
            "PartNumber",
            "BarCode",
            "DateLastReceived",
            "LotNumber",
            "SDSOnFile",
            "SDSNameURL",
            "SDSLocationURL",
            "Image",
            "DateModified",
            "ReorderLevel",
            "MinimumOrder",
            "StockUnitPrice",
            "RequestApprovedBy",
            "RequestApprovedDate",
        )
        optional_fields = [
            "Location",
            "Category",
            "Group",
            "Supplier",
        ]

        # exclude = ('Availability', 'FoundCount', 'ItemActiveNewOrder', 'SearchGroupGl', 'SearchMenu', 'SearchMenuGl', 'StockExtValue', 'TaxAmt', 'TotalStockValue',)

        # extra_kwargs = {'ItemDescription': {'allow_null': True, 'required': False, 'allow_blank': True}}

    def create(self, validated_data):
        request = self.context.get("request")
        item_name = validated_data.get("ItemName")
        bar_code = validated_data.get("BarCode")
        image = validated_data.pop("Image")

        print(type(validated_data.get("Location")))


        # location_objs = validated_data.pop("locations")
        # group_objs = validated_data.pop("groups")
        # category_objs = validated_data.pop("categories")
        # supplier_objs = validated_data.pop("suppliers")

        location_objs = validated_data.pop("Location", None)
        group_objs = validated_data.pop("Group", None)
        category_objs = validated_data.pop("Category", None)
        supplier_objs = validated_data.pop("Supplier", None)


        try:
            obj = Inventory.objects.get(ItemName=item_name)
        except Inventory.DoesNotExist:
            obj = None

        if obj is not None:
            raise serializers.ValidationError(
                "A product with the same name already exists in the selected group"
            )

        sds_name_url = validated_data.pop("SDSNameURL")
        sds_location_url = validated_data.pop("SDSLocationURL")
        lot_number = validated_data.pop("LotNumber")
        sds_on_file = validated_data.get("SDSOnFile")

        item = Inventory.objects.create(**validated_data, IsApproved=False)
        if location_objs is not None:
            item.Location.add(*location_objs)
        
        if group_objs is not None:
            item.Group.add(*group_objs)
        
        if category_objs is not None:
            item.Category.add(*category_objs)

        if supplier_objs is not None:
            item.Supplier.add(*supplier_objs)

        # for id in locations_ids:
        #     print(type(id))
        #     obj = Location.objects.get(id=id)
        #     item.Location.add(obj)

        if image is not None:
            item.Image = image

        item.save()

        # Creating sds record for the given product as well
        sds_record = InventorySDSRecord(
            SDSOnFile=sds_on_file,
            SDSNameURL=sds_name_url,
            SDSLocationURL=sds_location_url,
            IDRecord=item,
        )

        sds_record.save()

        return item

    def validate_RequestedBy(self, data):
        MyUser = get_user_model()
        try:
            new_data = MyUser.objects.get(email=data)
        except MyUser.DoesNotExist:
            return data
            # raise serializers.ValidationError("This email does not exist")
        return new_data

    def validate_RequestApprovedBy(self, data):
        MyUser = get_user_model()
        try:
            new_data = MyUser.objects.get(email=data)
        except MyUser.DoesNotExist:
            return data
            # raise serializers.ValidationError("This email does not exist")
        return new_data

    # def validate_Location(self, data):
    #     print("Valdating location")
    #     if(isinstance(data, str)):
    #         new_data = json.loads(data)
    #         print(type(new_data))
    #         return new_data
    #     return data

    # def validate_Group(self, data):
    #     print("Valdating group")
    #     if(isinstance(data, str)):
    #         new_data = json.loads(data)
    #         print(type(new_data))
    #         return new_data
    #     return data

    # def validate_Supplier(self, data):
    #     print("Valdating supplier")
    #     if(isinstance(data, str)):
    #         new_data = json.loads(data)
    #         print(type(new_data))
    #         return new_data
    #     return data

    # def validate_Category(self, data):
    #     print("Valdating category")
    #     if(isinstance(data, str)):
    #         new_data = json.loads(data)
    #         print(type(new_data))
    #         return new_data
    #     return data

    # def update(self, instance, validated_data):
    #     location_objs = validated_data.pop("Location", None)
    #     if location_objs is not None:
    #         instance.Location.remove(*instance.Location.all())
    #         for obj in location_objs:
    #             instance.Location.add(obj)

    #     instance.update(**validated_data)
    #     return instance


# class InventorySDSRecordSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = InventorySDSRecord
#         fields = "__all__"


class InventoryReportSerializer(serializers.ModelSerializer):
    currentDate = serializers.DateTimeField(format="%Y-%m-%d")
    RecordsFound = serializers.IntegerField()
    UnitsMeasure = serializers.CharField()
    UnitsOnHand = serializers.IntegerField()
    LastOrdered = serializers.DateTimeField(format="%Y-%m-%d")

    class Meta:
        model = Inventory
        fields = (
            "id",
            "currentDate",
            "RecordsFound",
            "ItemKnownAs",
            "ItemType",
            "Group",
            "Location",
            "ReorderLevel",
            "UnitsMeasure",
            "UnitsOnHand",
            "StockUnitPrice",
            "LastOrdered",
        )
        depth = 1


class CreateInventorySerializerNewWay(serializers.ModelSerializer):
    Image = HybridImageField(required=False)  # From DRF Extra Fields
    SDSLocationURL = serializers.CharField(required=False)
    SDSNameURL = serializers.CharField(required=False)
    ItemDescription = serializers.CharField(required=False)
    ItemKnownAs = serializers.CharField(required=False)
    UnitsOnHand = serializers.IntegerField(required=False)
    Stock = serializers.CharField(required=False)
    LotNumber = serializers.CharField(required=False)
    ThisRequest = serializers.CharField(required=False)

    class Meta:
        model = Inventory
        fields = (
            "DateEntered",
            "RequestedBy",
            "RequestedByDate",
            "ItemName",
            "ItemKnownAs",
            "ItemDescription",
            "Location",
            "Category",
            "Group",
            "ItemStatus",
            "DateLastOrdered",
            "DateLastUsed",
            # "ThisRequest",
            "Supplier",
            "ModelYear",
            "PartNumber",
            "BarCode",
            "DateLastReceived",
            "LotNumber",
            "SDSOnFile",
            "SDSNameURL",
            "SDSLocationURL",
            "Image",
            # "Stock",
            # "UnitsOnHand",
            "DateModified",
            "ReorderLevel",
            "MinimumOrder",
            "StockUnitPrice",
            "RequestApprovedBy",
            "RequestApprovedDate",
        )

    def create(self, validated_data):
        request = self.context.get("request")
        # Make name unique in a group
        item_name = validated_data.get("ItemName")
        bar_code = validated_data.get("BarCode")
        # group = validated_data.get("Group")

        try:
            obj = Inventory.objects.get(ItemName=item_name)
        except Inventory.DoesNotExist:
            obj = None

        if obj is not None:
            raise serializers.ValidationError(
                "A product with the same name already exists in the selected group"
            )

        try:
            obj = Inventory.objects.get(BarCode=bar_code)
        except Inventory.DoesNotExist:
            obj = None

        if obj is not None:
            raise serializers.ValidationError(
                "A product with the same barcode value already exists in the selected group"
            )

        MyUser = get_user_model()
        approved_by = validated_data.get("RequestApprovedBy")
        requested_by = validated_data.get("RequestedBy")
        product_is_approved = False

        sds_name_url = validated_data.pop("SDSNameURL")
        sds_location_url = validated_data.pop("SDSLocationURL")
        units_on_hand = validated_data.pop("UnitsOnHand")
        stock = validated_data.pop("Stock")
        lot_number = validated_data.pop("LotNumber")

        item = Inventory.objects.update_or_create(
            **validated_data, IsApproved=product_is_approved
        )

        item.save()
        return item

    def get_validation_exclusions(self):
        exclusions = super(
            CreateInventorySerializerNewWay, self
        ).get_validation_exclusions()
        return exclusions + ["owner"]


class InventorySerializerNewWay(serializers.ModelSerializer):
    Group = GroupSerializer()
    Location = LocationSerializer()
    Category = CategorySerializer()
    Supplier = SupplierSerializer()

    class Meta:
        model = Inventory
        fields = "__all__"

    def to_representation(self, instance):
        data = super(InventorySerializerNewWay, self).to_representation(instance)
        # manipulate data here
        context = {
            "message": "List of Inventory entries",
            "count": len(data),
            "data": data,
        }
        return context


class CreateInventorySerializer_BACKUP(serializers.ModelSerializer):
    Image = HybridImageField(required=False)  # From DRF Extra Fields
    SDSLocationURL = serializers.CharField(required=False)
    SDSNameURL = serializers.CharField(required=False)
    ItemDescription = serializers.CharField(required=False)
    ItemKnownAs = serializers.CharField(required=False)
    UnitsOnHand = serializers.IntegerField(required=False)
    Stock = serializers.CharField(required=False)
    LotNumber = serializers.CharField(required=False)
    ThisRequest = serializers.CharField(required=False)

    class Meta:
        model = Inventory
        fields = (
            "DateEntered",
            "RequestedBy",
            "RequestedByDate",
            "ItemName",
            "ItemKnownAs",
            "ItemDescription",
            "Location",
            "Category",
            "Group",
            "ItemStatus",
            "DateLastOrdered",
            "DateLastUsed",
            "ThisRequest",
            "Supplier",
            "ModelYear",
            "PartNumber",
            "BarCode",
            "DateLastReceived",
            "LotNumber",
            "SDSOnFile",
            "SDSNameURL",
            "SDSLocationURL",
            "Image",
            "Stock",
            "UnitsOnHand",
            "DateModified",
            "ReorderLevel",
            "MinimumOrder",
            "StockUnitPrice",
            "RequestApprovedBy",
            "RequestApprovedDate",
        )

    def create(self, validated_data):
        request = self.context.get("request")
        # Make name unique in a group
        item_name = validated_data.get("ItemName")
        bar_code = validated_data.get("BarCode")
        # group = validated_data.get("Group")

        try:
            obj = Inventory.objects.get(ItemName=item_name)
        except Inventory.DoesNotExist:
            obj = None

        if obj is not None:
            raise serializers.ValidationError(
                "A product with the same name already exists in the selected group"
            )

        try:
            obj = Inventory.objects.get(BarCode=bar_code)
        except Inventory.DoesNotExist:
            obj = None

        if obj is not None:
            raise serializers.ValidationError(
                "A product with the same barcode value already exists in the selected group"
            )

        MyUser = get_user_model()
        approved_by = validated_data.get("RequestApprovedBy")
        requested_by = validated_data.get("RequestedBy")
        product_is_approved = False

        # if requested_by != "" or requested_by != None:
        #     try:
        #         user_requested_by = MyUser.objects.get(id=requested_by)
        #     except MyUser.DoesNotExist:
        #         user_requested_by = None

        #     if not user_requested_by:
        #         raise serializers.ValidationError(
        #             "User id provided to requesting user is not valid"
        #         )

        # # If ApprovedBy is provided
        # # Checking if it exists. If it does, can it approve. If not raise error
        # if approved_by != "" or approved_by != None:
        #     try:
        #         user_approved_by = MyUser.objects.get(id=approved_by)
        #     except MyUser.DoesNotExist:
        #         user_approved_by = None

        #     if not user_approved_by:
        #         raise serializers.ValidationError(
        #             "User id provided to approving user is not valid"
        #         )

        #     if user_approved_by.is_admin == True:
        #         product_is_approved = True

        #     else:
        #         raise serializers.ValidationError(
        #             "User doesn't have permission to approve the product"
        #         )

        # sds_file_name = validated_data.pop("SDSFileName")

        sds_name_url = validated_data.pop("SDSNameURL")
        sds_location_url = validated_data.pop("SDSLocationURL")
        units_on_hand = validated_data.pop("UnitsOnHand")
        stock = validated_data.pop("Stock")
        # this_request = validated_data.pop("ThisRequest")
        lot_number = validated_data.pop("LotNumber")
        # date_last_received = validated_data.pop("DateLastReceived")
        # validated_data["Location"] = int(validated_data["Location"])

        item = Inventory.objects.update_or_create(
            **validated_data, IsApproved=product_is_approved
        )

        item.save()
        return item

    def validate(self, data):
        """
        Check that the start is before the stop.
        """
        if data["DateEntered"] == "" or data["DateEntered"] is None:
            pass
        if data["RequestedBy"] == "" or data["RequestedBy"] is None:
            pass

        return data


class UpdateInventorySerializer(serializers.ModelSerializer):
    Image = HybridImageField(required=False, allow_null=True)  # From DRF Extra Fields
    SDSLocationURL = serializers.CharField(required=False)
    SDSNameURL = serializers.CharField(required=False)
    ItemDescription = serializers.CharField(
        required=False, allow_null=True, allow_blank=True
    )
    ItemKnownAs = serializers.CharField(
        required=False, allow_null=True, allow_blank=True
    )
    LotNumber = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    DateEntered = serializers.DateTimeField(required=False, allow_null=True)
    ItemKnownAs = serializers.CharField(
        required=False, allow_null=True, allow_blank=True
    )
    DateLastOrdered = serializers.DateTimeField(required=False, allow_null=True)
    DateLastUsed = serializers.DateTimeField(required=False, allow_null=True)
    ModelYear = serializers.IntegerField(required=False, allow_null=True)
    PartNumber = serializers.CharField(
        required=False, allow_null=True, allow_blank=True
    )
    BarCode = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    DateLastReceived = serializers.DateTimeField(required=False, allow_null=True)
    LotNumber = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    SDSOnFile = serializers.BooleanField(default=False, required=False, allow_null=True)
    SDSNameURL = serializers.CharField(
        required=False, allow_null=True, allow_blank=True
    )
    SDSLocationURL = serializers.CharField(
        required=False, allow_null=True, allow_blank=True
    )
    DateModified = serializers.DateTimeField(required=False, allow_null=True)
    ReorderLevel = serializers.FloatField(required=False, allow_null=True)
    MinimumOrder = serializers.FloatField(required=False, allow_null=True)
    StockUnitPrice = serializers.FloatField(required=False, allow_null=True)
    RequestedBy = serializers.IntegerField(required=False, allow_null=True)
    RequestedByDate = serializers.DateTimeField(required=False, allow_null=True)
    RequestApprovedBy = serializers.IntegerField(required=False, allow_null=True)
    RequestApprovedDate = serializers.DateTimeField(required=False, allow_null=True)

    class Meta:
        model = Inventory
        fields = (
            "DateEntered",
            "RequestedBy",
            "RequestedByDate",
            "ItemName",
            "ItemKnownAs",
            "ItemDescription",
            "Location",
            "Category",
            "Group",
            "ItemStatus",
            "DateLastOrdered",
            "DateLastUsed",
            "Supplier",
            "ModelYear",
            "PartNumber",
            "BarCode",
            "DateLastReceived",
            "LotNumber",
            "SDSOnFile",
            "SDSNameURL",
            "SDSLocationURL",
            "Image",
            "DateModified",
            "ReorderLevel",
            "MinimumOrder",
            "StockUnitPrice",
            "RequestApprovedBy",
            "RequestApprovedDate",
        )

        # exclude = ('Availability', 'FoundCount', 'ItemActiveNewOrder', 'SearchGroupGl', 'SearchMenu', 'SearchMenuGl', 'StockExtValue', 'TaxAmt', 'TotalStockValue',)

        # extra_kwargs = {'ItemDescription': {'allow_null': True, 'required': False, 'allow_blank': True}}

    def update(self, validated_data):
        item = Inventory.objects.update(**validated_data)
        item.save()
        return item
