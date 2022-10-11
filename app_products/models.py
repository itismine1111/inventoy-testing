from django.db import models
import uuid
from django.contrib.auth import get_user_model

# Create your models here.

class Group(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return f'{self.name} - {self.id}'


class Location(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return f'{self.name} - {self.id}'


class Category(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return f'{self.name} - {self.id}'

    class Meta:
        verbose_name_plural = "Categories"


class Supplier(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return f'{self.name} - {self.id}'

    class Meta:
        verbose_name_plural = "Suppliers"


class UnitsMeasure(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return f'{self.name} - {self.id}'



def get_default_profile_image():
    return "default_images/default_profile_image.png"

def get_product_image_filepath(instance, filename):
    ext = filename.split('.')[-1]
    newfilename = '{}.{}'.format(instance.pk, ext)
    # newfilename = f'product_image_{instance.pk}'
    return f'product/{instance.pk}/{newfilename}'

def get_qr_image_filepath(self, filename):
    newfilename = f'qr_image_{self.pk}'
    return f'product/{self.pk}/{newfilename}'

def get_barcode_image_filepath(self, filename):
    newfilename = f'barcode_image_{self.pk}'
    return f'product/{self.pk}/{newfilename}'



class Inventory(models.Model):
    """
        This class defines the db fields for 
        [] Inventory Product Details.
        [] Purchase Orders for Inventory Products.
        [] Purchase Approval for a purchase order.
    """
    # Unstored Field (Calculated whenever necessery)
    Availability = models.CharField(max_length=255, null=True, blank=True)
    BarCode = models.CharField(max_length=255, blank=True, null=True)
    Category = models.ManyToManyField(Category)
    # Category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    DateEntered = models.DateTimeField(blank=True, null=True)
    DateExpired = models.DateTimeField(blank=True, null=True)
    DateLastOrdered = models.DateTimeField(blank=True, null=True)
    DateLastReceived = models.DateTimeField(blank=True, null=True)
    # Lookup field (Find value from last transaction of InventoryStockTransaction)
    DateLastUsed = models.DateTimeField(blank=True, null=True)
    # ?
    DateModified = models.DateTimeField(auto_now=True, blank=True, null=True)
    DeliveryCharge = models.FloatField(null=True, blank=True)
    FoundCount = models.FloatField(null=True, blank=True)
    Group = models.ManyToManyField(Group)
    # Group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    Image = models.ImageField(max_length=255, upload_to=get_product_image_filepath, null=True, blank=True, default=get_default_profile_image)
    ItemDescription = models.TextField(blank=True, null=True)
    # ItemName is unique in a category
    ItemName = models.CharField(max_length=255, blank=True, null=True)
    # Calculate when a new order for product is app
    ItemActiveNewOrder = models.CharField(max_length=255, blank=True, null=True)
    # Same as item Name
    ItemKnownAs = models.CharField(max_length=255, blank=True, null=True)
    STATUS_CHOICES =(
        ("active", "Active"),
        ("inactive", "In-active"),
        ("expired", "Expired"),
    )
    ItemStatus = models.CharField(max_length = 20, choices=STATUS_CHOICES, default='active')
    ItemType = models.CharField(max_length=255, blank=True, null=True)
    # Location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    Location = models.ManyToManyField(Location)
    Manufacturer = models.CharField(max_length=255, blank=True, null=True)
    MinimumOrder = models.FloatField(null=True, blank=True)
    ModelYear = models.IntegerField(null=True, blank=True)
    PartNumber = models.CharField(max_length=255, blank=True, null=True)
    RecordActive = models.IntegerField(null=True, blank=True)
    # RecordFlag
    # RecordFlagCalc
    ReorderLevel = models.FloatField(null=True, blank=True)
    RequestApprovedBy = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL,  null=True, related_name='request_approved_by')
    RequestApprovedDate = models.DateTimeField(blank=True, null=True)
    RequestedBy = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name='requested_by')
    RequestedByDate = models.DateTimeField(blank=True, null=True)
    SearchGroupGl = models.CharField(max_length=255, blank=True, null=True)
    SearchMenu = models.CharField(max_length=255, blank=True, null=True)
    SearchMenuGl = models.CharField(max_length=255, blank=True, null=True)
    # Unstored (Calculated when required)
    StockExtValue = models.FloatField(null=True, blank=True)
    StockUnitPrice = models.FloatField(null=True, blank=True)
    TaxAmt = models.FloatField(null=True, blank=True)
    TaxRate = models.FloatField(null=True, blank=True, default=0.925)
    Taxable = models.CharField(max_length=255, blank=True, null=True)
    TotalStockValue = models.FloatField(null=True, blank=True)  
    Supplier = models.ManyToManyField(Supplier)
    # Supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)
    IsApproved = models.BooleanField(default=False, blank=True, null=True)
    SDSOnFile = models.BooleanField(null=False, blank=False, default=False)
    # UnitsMeasure = models.CharField(max_length=255, null=True, blank=True)
    UnitsMeasure = models.ForeignKey(UnitsMeasure, on_delete=models.SET_NULL, null=True, blank=True)


    class Meta:
        verbose_name_plural = "Inventories"

    def __str__(self):
        return f'{self.ItemName} - {self.id}'



class InventoryStockTransaction(models.Model):
    """
        This class defines the db fields for.
        [] All the inventory products that are coming in and going out of different locations.
        [] We are going to be storing the quantities taken in and out.
    """
    DateTransaction = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    Description = models.TextField(blank=True, null=True)
    IDRecord = models.ForeignKey(Inventory, on_delete=models.SET_NULL, null=True)
    LotNumber = models.CharField(max_length=255, blank=True, null=True)
    Type = models.CharField(max_length=255, blank=True, null=True)
    TypeId = models.CharField(max_length=255, blank=True, null=True)
    Units = models.FloatField(null=True, blank=True)
    UnitsInOut = models.IntegerField(null=True, blank=True)
    # UnitsMeasure = models.CharField(max_length=255, null=True, blank=True)
    UnitsMeasure = models.ForeignKey(UnitsMeasure, on_delete=models.SET_NULL, null=True, blank=True)


class InventorySDSRecord(models.Model):
    """
        This class defines the db fields for
        [] The information about Safety Data Sheets associated with an inventory product
    """
    BarCode = models.CharField(max_length=255, blank=True, null=True)
    DateEntered = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    IDRecord = models.ForeignKey(Inventory, on_delete=models.SET_NULL, null=True)
    SDSCasNo = models.CharField(max_length=5, null=True, blank=True)
    SDSComponent = models.CharField(max_length=5, null=True, blank=True)
    SDSLocationURL = models.TextField(blank=True, null=True)
    SDSNameURL = models.TextField(blank=True, null=True)
    SDSOnFile = models.TextField(blank=True, null=True)

