from django.urls import path
from .views import (
    # Not used / Random
    GetAllSearchMenuItemsList,
    GetAllSearchMenuItemsDict,
    InvnetoryCreateUpdateGet,
    GetSearchItems,
    # Group view functions
    GetAllGroups,
    CreateGroup,
    UpdateGroup,
    DeleteGroup,
    GetGroupDetails,
    # Location view functions
    GetAllLocations,
    CreateLocation,
    UpdateLocation,
    DeleteLocation,
    GetLocationDetails,
    # Category view functions
    GetAllCategories,
    CreateCategory,
    UpdateCategory,
    DeleteCategory,
    GetCategoryDetails,
    # Supplier view functions
    GetAllSuppliers,
    CreateSupplier,
    UpdateSupplier,
    DeleteSupplier,
    GetSupplierDetails,
    # Unit Measure view functions
    GetAllUnitsMeasure,
    CreateUnitsMeasure,
    UpdateUnitsMeasure,
    DeleteUnitsMeasure,
    GetUnitsMeasureDetails,
    # Inventory view functions
    CreateInventory,
    UpdateInventory,
    GetProducts,
    GetProductsWithFilters,
    GetAllProducts,
    GetProductDetails,
    GetUnApprovedProducts,
    PostApproveInventory,
    GetProductsSortedByLocations,
    InventoryReportDetails,
    InventoryReportList,
    DeleteInventory,
    # Inventory Stock Transaction view functions
    GetInventoryStockTransactionForProduct,
    PostInventoryStockTransactionIn,
    PostInventoryStockTransactionOut,
    PostInventoryStockTransaction,
    DeleteStockTransactionRecord,
    UpdateInventoryStockTransaction,
    # Inventory SDS Recoord view functions
    InventorySDSRecordList,
    InventorySDSRecordDetails,
    GetSDSRecordDetailsFromProductId,
    UpdateSDSRecord,
    CreateSDSRecord,
)


urlpatterns = [
    # Not Used / Random
    path(
        "get-all-search-menu-items-list/",
        GetAllSearchMenuItemsList.as_view(),
        name="get-all-search-menu-items-list",
    ),
    path(
        "get-all-search-menu-items-dict/",
        GetAllSearchMenuItemsDict.as_view(),
        name="get-all-search-menu-items-dict",
    ),
    path("get-search-items/", GetSearchItems.as_view(), name="get-search-items"),
    path("new-inventory/", InvnetoryCreateUpdateGet.as_view(), name="new-inventory"),
    #  Group Urls
    path("get-all-groups/", GetAllGroups.as_view(), name="get-all-groups"),
    path("create-group/", CreateGroup.as_view(), name="create-group"),
    path("update-group/<int:pk>/", UpdateGroup.as_view(), name="update-group"),
    path("delete-group/<int:pk>/", DeleteGroup.as_view(), name="delete-group"),
    path(
        "get-group-details/<int:pk>/",
        GetGroupDetails.as_view(),
        name="get-group-details",
    ),
    # Location Urls
    path("get-all-locations/", GetAllLocations.as_view(), name="get-all-locations"),
    path("create-location/", CreateLocation.as_view(), name="create-location"),
    path("update-location/<int:pk>/", UpdateLocation.as_view(), name="update-location"),
    path("delete-location/<int:pk>/", DeleteLocation.as_view(), name="delete-location"),
    path(
        "get-location-details/<int:pk>/",
        GetLocationDetails.as_view(),
        name="get-location-details",
    ),
    # Category Urls
    path("get-all-categories/", GetAllCategories.as_view(), name="get-all-categories"),
    path("create-category/", CreateCategory.as_view(), name="create-category"),
    path("update-category/<int:pk>/", UpdateCategory.as_view(), name="update-category"),
    path("delete-category/<int:pk>/", DeleteCategory.as_view(), name="delete-category"),
    path(
        "get-category-details/<int:pk>/",
        GetCategoryDetails.as_view(),
        name="get-category-details",
    ),
    # Supplier Urls
    path("get-all-suppliers/", GetAllSuppliers.as_view(), name="get-all-suppliers"),
    path("create-supplier/", CreateSupplier.as_view(), name="create-supplier"),
    path("update-supplier/<int:pk>/", UpdateSupplier.as_view(), name="update-supplier"),
    path("delete-supplier/<int:pk>/", DeleteSupplier.as_view(), name="delete-supplier"),
    path(
        "get-supplier-details/<int:pk>/",
        GetSupplierDetails.as_view(),
        name="get-supplier-details",
    ),
    # Units Measutre urls
    path(
        "get-all-units-measure/",
        GetAllUnitsMeasure.as_view(),
        name="get-all-units-measure",
    ),
    path(
        "create-units-measure/",
        CreateUnitsMeasure.as_view(),
        name="create-units-measure",
    ),
    path(
        "update-units-measure/<int:pk>/",
        UpdateUnitsMeasure.as_view(),
        name="update-units-measure",
    ),
    path(
        "delete-units-measure/<int:pk>/",
        DeleteUnitsMeasure.as_view(),
        name="delete-units-measure",
    ),
    path(
        "get-units-measure-details/<int:pk>/",
        GetUnitsMeasureDetails.as_view(),
        name="get-units-measure-details",
    ),
    # Inventory Urls
    path("create-inventory/", CreateInventory.as_view(), name="create-inventory"),
    path(
        "update-inventory/<int:pk>/", UpdateInventory.as_view(), name="update-inventory"
    ),
    path("get-products/", GetProducts.as_view(), name="get-products"),
    path("get-product/<int:pk>/", GetProductDetails.as_view(), name="get-product"),
    path(
        "get-products-with-filters/",
        GetProductsWithFilters.as_view(),
        name="get-products-with-filters",
    ),
    path("get-all-products/", GetAllProducts.as_view(), name="get-all-products"),
    path(
        "get-products-sorted-by-location/",
        GetProductsSortedByLocations.as_view(),
        name="get-products-sorted-by-location",
    ),
    path(
        "get-unapproved-products/",
        GetUnApprovedProducts.as_view(),
        name="get-unapproved-products",
    ),
    path(
        "post-approve-product/",
        PostApproveInventory.as_view(),
        name="post-approve-product",
    ),
    path(
        "inventory-report/<int:pk>/",
        InventoryReportDetails.as_view(),
        name="inventory-report-details",
    ),
    path(
        "inventory-report/", InventoryReportList.as_view(), name="inventory-report-list"
    ),
    path(
        "delete-inventory/<int:pk>/", DeleteInventory.as_view(), name="delete-inventory"
    ),
    # Stock Transaction Urls
    path(
        "get-inventory-stock-transaction/<int:id>/",
        GetInventoryStockTransactionForProduct.as_view(),
        name="get-inventory-stock-transaction",
    ),
    path(
        "post-inventory-stock-transaction/in/",
        PostInventoryStockTransactionIn.as_view(),
        name="post-inventory-stock-transaction",
    ),
    path(
        "post-inventory-stock-transaction/out/",
        PostInventoryStockTransactionOut.as_view(),
        name="post-inventory-stock-transaction",
    ),
    path(
        "post-inventory-stock-transaction/<str:action>/<int:id>/",
        PostInventoryStockTransaction.as_view(),
        name="post-inventory-stock-transaction",
    ),
    path(
        "delete-inventory-stock-transaction/<int:pk>/",
        DeleteStockTransactionRecord.as_view(),
        name="delete-inventory-stock-transaction",
    ),
    path(
        "update-inventory-stock-transaction/<int:pk>/",
        UpdateInventoryStockTransaction.as_view(),
        name="update-inventory-stock-transaction",
    ),
    # Inventory SDS Record Urls
    path(
        "inventory-sds-record/",
        InventorySDSRecordList.as_view(),
        name="inventory-sds-record-list",
    ),
    path(
        "inventory-sds-record/<int:pk>/",
        InventorySDSRecordDetails.as_view(),
        name="inventory-sds-record-detail",
    ),
    path(
        "inventory-sds-record-for-product/<int:product_id>/",
        GetSDSRecordDetailsFromProductId.as_view(),
        name="inventory-sds-record-detail-for-product",
    ),
    path(
        "update-sds-record/<int:pk>/",
        UpdateSDSRecord.as_view(),
        name="update-sds-record",
    ),
    path(
        "create-sds-record/",
        CreateSDSRecord.as_view(),
        name="create-sds-record",
    ),
]
