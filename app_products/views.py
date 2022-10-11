from datetime import datetime
import json 

from django.db.models import Q

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework import generics
from rest_framework import mixins
from rest_framework.generics import GenericAPIView

from django_filters import rest_framework as filters


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

from .serializers import (
    InventorySerializer,
    GroupSerializer,
    LocationSerializer,
    CategorySerializer,
    StatusSerializer,
    SupplierSerializer,
    CreateInventorySerializer,
    InventoryStockTransactionSerializer,
    InventorySDSRecordSerializer,
    InventoryReportSerializer,
    InventorySerializerNewWay,
    UpdateInventorySerializer,
    UnitsMeasureSerializer,
)

from .filters import InventoryFilter


class GetAllSearchMenuItemsList(APIView):
    permission_classes = [AllowAny]

    def get(self, request):

        # Users should be authenticated
        if not (request.user and request.user.is_authenticated):
            return Response(
                {
                    "success": False,
                    "message": "Authentication failed",
                    "data": {},
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        context = []
        try:
            locations_obj = Location.objects.all()
            categories_obj = Category.objects.all()
            groups_obj = Group.objects.all()
            # status_obj = Status.objects.all()

            if (
                (locations_obj is not None)
                and (groups_obj is not None)
                and (categories_obj is not None)
            ):
                location_serializer = LocationSerializer(locations_obj, many=True)
                group_serializer = GroupSerializer(groups_obj, many=True)
                category_serializer = CategorySerializer(categories_obj, many=True)
                # status_serializer = StatusSerializer(status_obj, many=True)

                for item in group_serializer.data:
                    context.append(item)

                for item in location_serializer.data:
                    context.append(item)

                for item in category_serializer.data:
                    context.append(item)

                # for item in status_serializer.data:
                #     context.append(item)

                return Response(
                    {
                        "success": True,
                        "message": "List of all the Groups, Locations, Categories, Status",
                        "data": context,
                    },
                    status=status.HTTP_200_OK,
                )

            return Response(
                {
                    "success": False,
                    "message": "Some or any of the search menu items does not exist",
                    "data": {},
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception as e:
            print(e)


class GetAllSearchMenuItemsDict(APIView):
    permission_classes = [AllowAny]

    def get(self, request):

        # Users should be authenticated
        if not (request.user and request.user.is_authenticated):
            return Response(
                {
                    "success": False,
                    "message": "Authentication failed",
                    "data": {},
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            locations_obj = Location.objects.all()
            categories_obj = Category.objects.all()
            groups_obj = Group.objects.all()
            # status_obj = Status.objects.all()
            status_obj = [
                {"id": "0", "name": "inactive"},
                {"id": "1", "name": "active"},
            ]
            suppliers_obj = Supplier.objects.all()

            if (
                (locations_obj is not None)
                and (groups_obj is not None)
                and (categories_obj is not None)
                and (suppliers_obj is not None)
            ):
                location_serializer = LocationSerializer(locations_obj, many=True)
                group_serializer = GroupSerializer(groups_obj, many=True)
                category_serializer = CategorySerializer(categories_obj, many=True)
                status_serializer = StatusSerializer(status_obj, many=True)
                supplier_serializer = SupplierSerializer(suppliers_obj, many=True)

                return Response(
                    {
                        "success": True,
                        "message": "List of all the Groups, Categories, Locations, Suppliers and Status",
                        "data": {
                            "groups": {
                                "name": "Groups",
                                "count": len(group_serializer.data),
                                "list": group_serializer.data,
                            },
                            "categories": {
                                "name": "Categories",
                                "count": len(category_serializer.data),
                                "list": category_serializer.data,
                            },
                            "locations": {
                                "name": "Locations",
                                "count": len(location_serializer.data),
                                "list": location_serializer.data,
                            },
                            "status": {
                                "name": "Status",
                                "count": len(status_serializer.data),
                                "list": status_serializer.data,
                            },
                            "suppliers": {
                                "name": "Suppliers",
                                "count": len(supplier_serializer.data),
                                "list": supplier_serializer.data,
                            },
                        },
                    },
                    status=status.HTTP_200_OK,
                )

            return Response(
                {
                    "success": False,
                    "message": "Some or any of the search menu items does not exist",
                    "data": {},
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception as e:
            print(e)


# Group Model API's
class GetAllGroups(APIView):
    permission_classes = [AllowAny]

    def get(self, request):

        # Users should be authenticated
        if not (request.user and request.user.is_authenticated):
            return Response(
                {
                    "success": False,
                    "message": "Authentication failed",
                    "data": {},
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        name = request.GET.get("name", "")
        sort = request.GET.get("sort", "")

        try:
            if name == "" or not name:
                groups_obj = Group.objects.all()
            else:
                groups_obj = Group.objects.filter(name__startswith=name)

            if sort == "" or sort == "asc":
                groups_obj = groups_obj.order_by("name")
            elif sort == "dec":
                groups_obj = groups_obj.order_by("-name")

            if groups_obj is not None:
                serializer = GroupSerializer(groups_obj, many=True)

                return Response(
                    {
                        "success": True,
                        "message": "List of all the Groups",
                        "data": {
                            "count": len(serializer.data),
                            "list": serializer.data,
                        },
                    },
                    status=status.HTTP_200_OK,
                )

            return Response(
                {
                    "success": False,
                    "message": "No groups exist",
                    "data": {},
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception as e:
            print(e)


class CreateGroup(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        if not (request.user and request.user.is_authenticated):
            return Response(
                {
                    "success": False,
                    "message": "Authentication failed",
                    "data": {},
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "Group created",
                    "data": serializer.data,
                },
                status=201,
            )

        return Response(
            {
                "success": False,
                "message": "Error occured",
                "data": serializer.errors,
            },
            status=400,
        )


class UpdateGroup(APIView):
    permission_classes = [AllowAny]

    def post(self, request, pk):
        if not (request.user and request.user.is_authenticated):
            return Response(
                {
                    "success": False,
                    "message": "Authentication failed",
                    "data": {},
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            item = Group.objects.get(id=pk)
        except Group.DoesNotExist:
            item = None

        if item is not None:
            serializer = GroupSerializer(instance=item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "success": True,
                        "message": "Group Updated",
                        "data": serializer.data,
                    },
                    status=201,
                )

        return Response(
            {
                "success": False,
                "message": "No Group with the given id exists",
                "data": serializer.errors,
            },
            status=400,
        )


class DeleteGroup(APIView):
    permission_classes = [AllowAny]

    def post(self, request, pk):
        if not (request.user and request.user.is_authenticated):
            return Response(
                {
                    "success": False,
                    "message": "Authentication failed",
                    "data": {},
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            item = Group.objects.get(id=pk)
        except Group.DoesNotExist:
            item = None

        if item is not None:
            item.delete()
            return Response(
                {
                    "success": True,
                    "message": "Group Deleted",
                    "data": {},
                },
                status=200,
            )

        return Response(
            {
                "success": False,
                "message": "No Group with the given id exists",
                "data": {},
            },
            status=400,
        )


class GetGroupDetails(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        if not (request.user and request.user.is_authenticated):
            return Response(
                {
                    "success": False,
                    "message": "Authentication failed",
                    "data": {},
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            item = Group.objects.get(id=pk)
        except Group.DoesNotExist:
            item = None

        if item is not None:
            serializer = GroupSerializer(instance=item)
            return Response(
                {
                    "success": True,
                    "message": "Details for the Group",
                    "data": serializer.data,
                },
                status=201,
            )

        return Response(
            {
                "success": False,
                "message": "No Group with the given id exists",
                "data": {},
            },
            status=400,
        )


# UnitsMeasure Model API's
class GetAllUnitsMeasure(APIView):
    permission_classes = [AllowAny]

    def get(self, request):

        # Users should be authenticated
        if not (request.user and request.user.is_authenticated):
            return Response(
                {
                    "success": False,
                    "message": "Authentication failed",
                    "data": {},
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        name = request.GET.get("name", "")
        sort = request.GET.get("sort", "")

        try:
            if name == "" or not name:
                units_measure_obj = UnitsMeasure.objects.all()
            else:
                units_measure_obj = UnitsMeasure.objects.filter(name__startswith=name)

            if sort == "" or sort == "asc":
                units_measure_obj = units_measure_obj.order_by("name")
            elif sort == "dec":
                units_measure_obj = units_measure_obj.order_by("-name")

            if units_measure_obj is not None:
                serializer = UnitsMeasureSerializer(units_measure_obj, many=True)

                return Response(
                    {
                        "success": True,
                        "message": "List of all the Unit Measures",
                        "data": {
                            "count": len(serializer.data),
                            "list": serializer.data,
                        },
                    },
                    status=status.HTTP_200_OK,
                )

            return Response(
                {
                    "success": False,
                    "message": "No Units Measure exist",
                    "data": {},
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception as e:
            print(e)


class CreateUnitsMeasure(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        if not (request.user and request.user.is_authenticated):
            return Response(
                {
                    "success": False,
                    "message": "Authentication failed",
                    "data": {},
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = UnitsMeasureSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "Units Measure created",
                    "data": serializer.data,
                },
                status=201,
            )

        return Response(
            {
                "success": False,
                "message": "Error occured",
                "data": serializer.errors,
            },
            status=400,
        )


class UpdateUnitsMeasure(APIView):
    permission_classes = [AllowAny]

    def post(self, request, pk):
        if not (request.user and request.user.is_authenticated):
            return Response(
                {
                    "success": False,
                    "message": "Authentication failed",
                    "data": {},
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            item = UnitsMeasure.objects.get(id=pk)
        except UnitsMeasure.DoesNotExist:
            item = None

        if item is not None:
            serializer = UnitsMeasureSerializer(instance=item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "success": True,
                        "message": "Units Measure Updated",
                        "data": serializer.data,
                    },
                    status=201,
                )

        return Response(
            {
                "success": False,
                "message": "No Units Measure with the given id exists",
                "data": serializer.errors,
            },
            status=400,
        )


class DeleteUnitsMeasure(APIView):
    permission_classes = [AllowAny]

    def post(self, request, pk):
        if not (request.user and request.user.is_authenticated):
            return Response(
                {
                    "success": False,
                    "message": "Authentication failed",
                    "data": {},
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            item = UnitsMeasure.objects.get(id=pk)
        except UnitsMeasure.DoesNotExist:
            item = None

        if item is not None:
            item.delete()
            return Response(
                {
                    "success": True,
                    "message": "Units Measure Deleted",
                    "data": {},
                },
                status=200,
            )

        return Response(
            {
                "success": False,
                "message": "No Units Measure with the given id exists",
                "data": {},
            },
            status=400,
        )


class GetUnitsMeasureDetails(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        if not (request.user and request.user.is_authenticated):
            return Response(
                {
                    "success": False,
                    "message": "Authentication failed",
                    "data": {},
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            item = UnitsMeasure.objects.get(id=pk)
        except UnitsMeasure.DoesNotExist:
            item = None

        if item is not None:
            serializer = UnitsMeasureSerializer(instance=item)
            return Response(
                {
                    "success": True,
                    "message": "Details for the Units Measure",
                    "data": serializer.data,
                },
                status=201,
            )

        return Response(
            {
                "success": False,
                "message": "No Units Measure with the given id exists",
                "data": {},
            },
            status=400,
        )


# Location Model API's
class GetAllLocations(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # Users should be authenticated
        if not (request.user and request.user.is_authenticated):
            return Response(
                {
                    "success": False,
                    "message": "Authentication failed",
                    "data": {},
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        name = request.GET.get("name", "")
        sort = request.GET.get("sort", "")

        try:
            if name == "" or not name:
                locations_obj = Location.objects.all()
            else:
                locations_obj = Location.objects.filter(name__startswith=name)

            if sort == "" or sort == "asc":
                locations_obj = locations_obj.order_by("name")
            elif sort == "dec":
                locations_obj = locations_obj.order_by("-name")

            if locations_obj is not None:
                serializer = LocationSerializer(locations_obj, many=True)

                return Response(
                    {
                        "success": True,
                        "message": "List of all the Locations",
                        "data": {
                            "count": len(serializer.data),
                            "list": serializer.data,
                        },
                    },
                    status=status.HTTP_200_OK,
                )

            return Response(
                {
                    "success": False,
                    "message": "No locations exist",
                    "data": {},
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception as e:
            print(e)


class CreateLocation(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        if not (request.user and request.user.is_authenticated):
            return Response(
                {
                    "success": False,
                    "message": "Authentication failed",
                    "data": {},
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "Location created",
                    "data": serializer.data,
                },
                status=201,
            )

        return Response(
            {
                "success": False,
                "message": "Error occured",
                "data": serializer.errors,
            },
            status=400,
        )


class UpdateLocation(APIView):
    permission_classes = [AllowAny]

    def post(self, request, pk):
        if not (request.user and request.user.is_authenticated):
            return Response(
                {
                    "success": False,
                    "message": "Authentication failed",
                    "data": {},
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            item = Location.objects.get(id=pk)
        except Location.DoesNotExist:
            item = None

        if item is not None:
            serializer = LocationSerializer(instance=item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "success": True,
                        "message": "Location Updated",
                        "data": serializer.data,
                    },
                    status=201,
                )

        return Response(
            {
                "success": False,
                "message": "No Location with the given id exists",
                "data": serializer.errors,
            },
            status=400,
        )


class DeleteLocation(APIView):
    permission_classes = [AllowAny]

    def post(self, request, pk):
        if not (request.user and request.user.is_authenticated):
            return Response(
                {
                    "success": False,
                    "message": "Authentication failed",
                    "data": {},
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            item = Location.objects.get(id=pk)
        except Location.DoesNotExist:
            item = None

        if item is not None:
            item.delete()
            return Response(
                {
                    "success": True,
                    "message": "Location Deleted",
                    "data": {},
                },
                status=200,
            )

        return Response(
            {
                "success": False,
                "message": "No Location with the given id exists",
                "data": {},
            },
            status=400,
        )


class GetLocationDetails(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        if not (request.user and request.user.is_authenticated):
            return Response(
                {
                    "success": False,
                    "message": "Authentication failed",
                    "data": {},
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            item = Location.objects.get(id=pk)
        except Location.DoesNotExist:
            item = None

        if item is not None:
            serializer = LocationSerializer(instance=item)
            return Response(
                {
                    "success": True,
                    "message": "Details for the Location",
                    "data": serializer.data,
                },
                status=201,
            )

        return Response(
            {
                "success": False,
                "message": "No Location with the given id exists",
                "data": {},
            },
            status=400,
        )


# Category Model API's
class GetAllCategories(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # Users should be authenticated
        if not (request.user and request.user.is_authenticated):
            return Response(
                {
                    "success": False,
                    "message": "Authentication failed",
                    "data": {},
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        name = request.GET.get("name", "")
        sort = request.GET.get("sort", "")

        try:
            if name == "" or not name:
                categories_obj = Category.objects.all()
            else:
                categories_obj = Category.objects.filter(name__startswith=name)

            if sort == "" or sort == "asc":
                categories_obj = categories_obj.order_by("name")
            elif sort == "dec":
                categories_obj = categories_obj.order_by("-name")

            if categories_obj is not None:
                serializer = CategorySerializer(categories_obj, many=True)

                return Response(
                    {
                        "success": True,
                        "message": "List of all the Categories",
                        "data": {
                            "count": len(serializer.data),
                            "list": serializer.data,
                        },
                    },
                    status=status.HTTP_200_OK,
                )

            return Response(
                {
                    "success": False,
                    "message": "No categories exist",
                    "data": {},
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception as e:
            print(e)


class CreateCategory(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        if not (request.user and request.user.is_authenticated):
            return Response(
                {
                    "success": False,
                    "message": "Authentication failed",
                    "data": {},
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "Category created",
                    "data": serializer.data,
                },
                status=201,
            )

        return Response(
            {
                "success": False,
                "message": "Error occured",
                "data": serializer.errors,
            },
            status=400,
        )


class UpdateCategory(APIView):
    permission_classes = [AllowAny]

    def post(self, request, pk):
        if not (request.user and request.user.is_authenticated):
            return Response(
                {
                    "success": False,
                    "message": "Authentication failed",
                    "data": {},
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            item = Category.objects.get(id=pk)
        except Category.DoesNotExist:
            item = None

        if item is not None:
            serializer = CategorySerializer(instance=item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "success": True,
                        "message": "Category Updated",
                        "data": serializer.data,
                    },
                    status=201,
                )

        return Response(
            {
                "success": False,
                "message": "No Category with the given id exists",
                "data": serializer.errors,
            },
            status=400,
        )


class DeleteCategory(APIView):
    permission_classes = [AllowAny]

    def post(self, request, pk):
        if not (request.user and request.user.is_authenticated):
            return Response(
                {
                    "success": False,
                    "message": "Authentication failed",
                    "data": {},
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            item = Category.objects.get(id=pk)
        except Category.DoesNotExist:
            item = None

        if item is not None:
            item.delete()
            return Response(
                {
                    "success": True,
                    "message": "Category Deleted",
                    "data": {},
                },
                status=200,
            )

        return Response(
            {
                "success": False,
                "message": "No Category with the given id exists",
                "data": {},
            },
            status=400,
        )


class GetCategoryDetails(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        if not (request.user and request.user.is_authenticated):
            return Response(
                {
                    "success": False,
                    "message": "Authentication failed",
                    "data": {},
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            item = Category.objects.get(id=pk)
        except Category.DoesNotExist:
            item = None

        if item is not None:
            serializer = CategorySerializer(instance=item)
            return Response(
                {
                    "success": True,
                    "message": "Details for the Category",
                    "data": serializer.data,
                },
                status=201,
            )

        return Response(
            {
                "success": False,
                "message": "No Category with the given id exists",
                "data": {},
            },
            status=400,
        )


# Supplier Model API's
class GetAllSuppliers(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # Users should be authenticated
        if not (request.user and request.user.is_authenticated):
            return Response(
                {
                    "success": False,
                    "message": "Authentication failed",
                    "data": {},
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        name = request.GET.get("name", "")
        sort = request.GET.get("sort", "")

        try:
            if name == "" or not name:
                suppliers_obj = Supplier.objects.all()
            else:
                suppliers_obj = Supplier.objects.filter(name__startswith=name)

            if sort == "" or sort == "asc":
                suppliers_obj = suppliers_obj.order_by("name")
            elif sort == "dec":
                suppliers_obj = suppliers_obj.order_by("-name")

            if suppliers_obj is not None:
                serializer = SupplierSerializer(suppliers_obj, many=True)

                return Response(
                    {
                        "success": True,
                        "message": "List of all the Suppliers",
                        "data": {
                            "count": len(serializer.data),
                            "list": serializer.data,
                        },
                    },
                    status=status.HTTP_200_OK,
                )

            return Response(
                {
                    "success": False,
                    "message": "No suppliers exist",
                    "data": {},
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception as e:
            print(e)


class CreateSupplier(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        if not (request.user and request.user.is_authenticated):
            return Response(
                {
                    "success": False,
                    "message": "Authentication failed",
                    "data": {},
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = SupplierSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "Supplier created",
                    "data": serializer.data,
                },
                status=201,
            )

        return Response(
            {
                "success": False,
                "message": "Error occured",
                "data": serializer.errors,
            },
            status=400,
        )


class UpdateSupplier(APIView):
    permission_classes = [AllowAny]

    def post(self, request, pk):
        if not (request.user and request.user.is_authenticated):
            return Response(
                {
                    "success": False,
                    "message": "Authentication failed",
                    "data": {},
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            item = Supplier.objects.get(id=pk)
        except Supplier.DoesNotExist:
            item = None

        if item is not None:
            serializer = SupplierSerializer(instance=item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "success": True,
                        "message": "Supplier Updated",
                        "data": serializer.data,
                    },
                    status=201,
                )

        return Response(
            {
                "success": False,
                "message": "No Supplier with the given id exists",
                "data": serializer.errors,
            },
            status=400,
        )


class DeleteSupplier(APIView):
    permission_classes = [AllowAny]

    def post(self, request, pk):
        if not (request.user and request.user.is_authenticated):
            return Response(
                {
                    "success": False,
                    "message": "Authentication failed",
                    "data": {},
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            item = Supplier.objects.get(id=pk)
        except Supplier.DoesNotExist:
            item = None

        if item is not None:
            item.delete()
            return Response(
                {
                    "success": True,
                    "message": "Supplier Deleted",
                    "data": {},
                },
                status=200,
            )

        return Response(
            {
                "success": False,
                "message": "No Supplier with the given id exists",
                "data": {},
            },
            status=400,
        )


class GetSupplierDetails(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        # Users should be authenticated
        if not (request.user and request.user.is_authenticated):
            return Response(
                {
                    "success": False,
                    "message": "Authentication failed",
                    "data": {},
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            suppliers_obj = Supplier.objects.get(id=pk)
        except Supplier.DoesNotExist:
            suppliers_obj = None

        if suppliers_obj is not None:
            serializer = SupplierSerializer(suppliers_obj)

            return Response(
                {
                    "success": True,
                    "message": f"Details of Supplier: { suppliers_obj.id }",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {
                "success": False,
                "message": "No supplier with given id exists",
                "data": {},
            },
            status=status.HTTP_404_NOT_FOUND,
        )


# Some Random API's

class GetSearchItems(APIView):
    permission_classes = [AllowAny]

    def get(self, request):

        # Users should be authenticated
        if not (request.user and request.user.is_authenticated):
            return Response(
                {
                    "success": False,
                    "message": "Authentication failed",
                    "data": {},
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        search = self.request.GET.get("search", "")

        if search == "" or search is None:
            return Response(
                {
                    "success": True,
                    "message": "Inventory Product Details",
                    "data": [
                        "Groups",
                        "Categories",
                        "Locations",
                        "Status",
                        "Suppliers",
                    ],
                },
                status=status.HTTP_200_OK,
            )

        elif search.lower() == "groups":
            data = Group.objects.all()
            response_data = GroupSerializer(data, many=True).data
            message = "List of all groups"

        elif search.lower() == "categories":
            data = Category.objects.all()
            response_data = CategorySerializer(data, many=True).data
            message = "List of all categories"

        elif search.lower() == "locations":
            data = Location.objects.all()
            response_data = LocationSerializer(data, many=True).data
            message = "List of all locations"

        elif search.lower() == "status":
            data = [{"id": "0", "name": "inactive"}, {"id": "1", "name": "active"}]
            response_data = StatusSerializer(data, many=True).data
            message = "List of status"

        elif search.lower() == "suppliers":
            data = Supplier.objects.all()
            response_data = SupplierSerializer(data, many=True).data
            message = "List of all suppliers"

        return Response(
            {
                "success": True,
                "message": message,
                "data": {"count": len(response_data), "list": response_data},
            },
            status=status.HTTP_200_OK,
        )



# Inventory API's

class CreateInventory(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Users should be authenticated
        if not (request.user and request.user.is_authenticated):
            return Response(
                {
                    "success": False,
                    "message": "Authentication failed",
                    "data": {},
                },
                status=status.HTTP_403_FORBIDDEN,
            )


        # new_data = request.data.copy()

        # if(isinstance(new_data.get("Location"), str)):
        #     temp = json.loads(new_data['Location'])
        #     print("TYPE OF TEMP")
        #     print(type(temp))
        #     print(temp)

        #     new_data['Location'] = temp

            # for i in temp:
            #     print(i)
            #     new_data['Location'] = temp
            #     print("TYPE OF LOCATION")
            #     print(type(new_data['Location']))
            # new_data['Location'] = temp[0]
            # print(new_data["Location"])
            # print(type(new_data["Location"]))

        # if(isinstance(new_data.get("Category"), str)):
        #     temp = json.loads(new_data['Category'])
        #     for i in temp:
        #         print(i)
                # new_data['Category'].append(i)
            # new_data['Category'] = temp[0]

        # if(isinstance(new_data.get("Group"), str)):
        #     temp = json.loads(new_data['Group'])
        #     for i in temp:
        #         print(i)
                # new_data['Group'].append(i)
            # new_data['Group'] = temp[0]

        # if(isinstance(new_data.get("Supplier"), str)):
        #     temp = json.loads(new_data['Supplier'])
        #     for i in temp:
        #         print(i)
                # new_data['Supplier'].append(i
            # new_data['Supplier'] = temp[0]


        serializer = CreateInventorySerializer(
            data=request.data, context={"request": request}
        )
        print(serializer)

        if serializer.is_valid():
            serializer.save()

            new_inventory_obj = Inventory.objects.get(
                ItemName=serializer.data.get("ItemName")
            )
            new_inventory_obj_serializer = InventorySerializer(new_inventory_obj)
            return Response(
                {
                    "success": True,
                    "message": "Product created",
                    "data": new_inventory_obj_serializer.data,
                },
                status=201,
            )

        return Response(
            {
                "success": False,
                "message": "Error occured",
                "data": serializer.errors,
            },
            status=400,
        )


# class UpdateInventory(UpdateAPIView):
#     serializer_class = CreateInventorySerializer
#     lookup_field = "id"
#     lookup_url_kwarg = "id"
#     query_set = Inventory.objects.all()
#     permission_classes = [AllowAny, IsAuthenticated]

#     def post(self, request, pk):
#         if not (request.user and request.user.is_authenticated):
#             return Response(
#                 {
#                     "success": False,
#                     "message": "Authentication failed",
#                     "data": {},
#                 },
#                 status=status.HTTP_403_FORBIDDEN,
#             )

#         try:
#             item = Inventory.objects.get(id=pk)
#         except Inventory.DoesNotExist:
#             item = None

#         if item is not None:
#             # item = Inventory.objects.filter(id=pk).update(**request.data)
#             serializer = InventorySerializer(item)
#             if serializer.is_valid():
#                 serializer.update(instance=item)
#                 # item = Inventory.objects.get(id=pk).update(**request.data)
#                 return Response(
#                     {
#                         "success": True,
#                         "message": "Inventory Updated",
#                         "data": serializer.data,
#                     },
#                     status=201,
#                 )

#         return Response(
#             {
#                 "success": False,
#                 "message": "No Inventory with the given id exists",
#                 # "data": serializer.errors,
#                 "data": {},
#             },
#             status=400,
#         )


class UpdateInventory(APIView):
    permission_classes = [AllowAny]

    def post(self, request, pk):
        if not (request.user and request.user.is_authenticated):
            return Response(
                {
                    "success": False,
                    "message": "Authentication failed",
                    "data": {},
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            item = Inventory.objects.get(id=pk)
        except Inventory.DoesNotExist:
            item = None

        if item is not None:
            locations_objs = []
            categories_objs = []
            groups_objs = []
            suppliers_objs = []

            # request.data._mutable = True
            locations = request.data.pop('Location', None)
            categories = request.data.pop('Category', None)
            groups = request.data.pop('Group', None)
            suppliers = request.data.pop('Supplier', None)
            # request.data._mutable = False


            if locations is not None:
                for id in locations:
                    try:
                        id_obj = Location.objects.get(id=id)
                        locations_objs.append(id_obj)
                    except:
                        return Response(
                        {
                            "success": False,
                            "message": "Locations with the given id does not exist",
                            "data": {},
                            # "data": serializer.data,
                        },
                        status=400,
                    )
            
                    item.Location.set(locations_objs)

            if categories is not None:
                for id in categories:
                    try:
                        id_obj = Category.objects.get(id=id)
                        categories_objs.append(id_obj)
                    except:
                        return Response(
                        {
                            "success": False,
                            "message": "Categories with the given id does not exist",
                            "data": {},
                            # "data": serializer.data,
                        },
                        status=400,
                    )
            
                    item.Category.set(categories_objs)

            if groups is not None:
                for id in groups:
                    try:
                        id_obj = Group.objects.get(id=id)
                        groups_objs.append(id_obj)
                    except:
                        return Response(
                        {
                            "success": False,
                            "message": "Groups with the given id does not exist",
                            "data": {},
                            # "data": serializer.data,
                        },
                        status=400,
                    )
            
                    item.Group.set(groups_objs)


            if suppliers is not None:
                for id in suppliers:
                    try:
                        id_obj = Supplier.objects.get(id=id)
                        suppliers_objs.append(id_obj)
                    except:
                        return Response(
                        {
                            "success": False,
                            "message": "Suppliers with the given id does not exist",
                            "data": {},
                            # "data": serializer.data,
                        },
                        status=400,
                    )
            
                    item.Supplier.set(suppliers_objs)

            serializer = CreateInventorySerializer(instance=item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                # print(serializer.data.get("id"))
                return Response(
                    {
                        "success": True,
                        "message": "Inventory Updated",
                        "data": {},
                        # "data": serializer.data,
                    },
                    status=201,
                )
        else:
            return Response(
                    {
                        "success": False,
                        "message": "No invenentory with the given id exists",
                        "data": {},
                        # "data": serializer.data,
                    },
                    status=201,
                )

        return Response(
            {
                "success": False,
                "message": "Errors occurd while updating data",
                "data": serializer.errors,
            },
            status=400,
        )


class GetAllProducts(generics.ListAPIView):
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Inventory.objects.all()

        # group_id = self.request.query_params.get('group_id')
        # location_id = self.request.query_params.get('location_id')
        # category_id = self.request.query_params.get('category_id')
        # status = self.request.query_params.get('status')
        # search_name = self.request.query_params.get('search_name')

        group_id = self.request.query_params.get("group")
        location_id = self.request.query_params.get("location")
        category_id = self.request.query_params.get("category")
        status_id = self.request.query_params.get("status")
        search_name = self.request.query_params.get("search_name")
        supplier_id = self.request.query_params.get("supplier")
        barcode = self.request.query_params.get("barcode")

        if group_id:
            try:
                queryset = queryset.filter(Group__id=group_id)
            except Exception as e:
                print(e)

        elif category_id:
            try:
                queryset = queryset.filter(Category__id=category_id)
            except Exception as e:
                print(e)

        elif location_id:
            try:
                queryset = queryset.filter(Location__id=location_id)
            except Exception as e:
                print(e)

        elif status_id:
            try:
                if status_id == 0:
                    status = "inactive"
                else:
                    status = "active"

                queryset = queryset.filter(ItemStatus=status)
            except Exception as e:
                print(e)

        elif supplier_id:
            queryset = queryset.filter(Supplier__id=supplier_id)

        elif search_name:
            queryset = queryset.filter(
                Q(ItemName__icontains=search_name)
                | Q(ItemKnownAs__icontains=search_name)
            )

        elif barcode:
            queryset = queryset.filter(BarCode=barcode)

        return queryset

    def get(self, request):

        # Users should be authenticated
        if not (request.user and request.user.is_authenticated):
            return Response(
                {
                    "success": False,
                    "message": "Authentication failed",
                    "data": {},
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            inventory_objects = self.get_queryset()
            # inventory_objects = Inventory.objects.all()

            if inventory_objects is not None:
                serializer = InventorySerializer(inventory_objects, many=True)

                return Response(
                    {
                        "success": True,
                        "message": "List of the inventory Products",
                        "data": {
                            "count": len(serializer.data),
                            "list": serializer.data,
                        },
                    },
                    status=status.HTTP_200_OK,
                )

            return Response(
                {
                    "success": False,
                    "message": "No Products Present",
                    "data": {},
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception as e:
            print(e)


class GetProducts(generics.ListAPIView):
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Inventory.objects.filter(IsApproved=True)
        search_by = self.request.query_params.get("search_by", "")
        search = self.request.query_params.get("search", "")
        sort = self.request.query_params.get("sort", "")

        print(f"{search_by} + {search} + {sort}")

        if (
            search_by is None
            or search_by == ""
            or search is None
            or search == 0
            or search == "0"
        ):
            if sort is None or sort == "":
                pass
            else:
                if sort == "asc":
                    queryset = queryset.order_by("ItemName")
                elif sort == "dec":
                    queryset = queryset.order_by("-ItemName")

            return queryset

        search_by = search_by.lower()
        if search_by == "groups":
            try:
                queryset = queryset.filter(Group__id=search)
            except Exception as e:
                print(e)

        elif search_by == "categories":
            try:
                queryset = queryset.filter(Category__id=search)
            except Exception as e:
                print(e)

        elif search_by == "locations":
            try:
                queryset = queryset.filter(Location__id=search)
            except Exception as e:
                print(e)

        elif search_by == "status":
            try:
                if search == 0:
                    status = "inactive"
                else:
                    status = "active"

                queryset = queryset.filter(ItemStatus=status)
            except Exception as e:
                print(e)

        elif search_by == "name":
            queryset = queryset.filter(
                Q(ItemName__icontains=search) | Q(ItemKnownAs__icontains=search)
            )

        elif search_by == "suppliers":
            try:
                queryset = queryset.filter(Supplier__id=search)
            except Exception as e:
                print(e)

        if sort == "asc":
            queryset = queryset.order_by("ItemName")
            print("ASCENDING")
        elif sort == "dec":
            print("DESCENDING")
            queryset = queryset.order_by("-ItemName")

        return queryset

    def get(self, request):

        # Users should be authenticated
        if not (request.user and request.user.is_authenticated):
            return Response(
                {
                    "success": False,
                    "message": "Authentication failed",
                    "data": {},
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            inventory_objects = list(self.get_queryset())

            if inventory_objects is not None and len(inventory_objects) != 0:
                serializer = InventorySerializer(inventory_objects, many=True)

                return Response(
                    {
                        "success": True,
                        "message": "List of the inventory Products",
                        "data": {
                            "count": len(serializer.data),
                            "list": serializer.data,
                        },
                    },
                    status=status.HTTP_200_OK,
                )

            return Response(
                {
                    "success": True,
                    "message": "No Products Present",
                    "data": {
                        "count": 0,
                        "list": "",
                    },
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            print(e)


class GetProductsWithFilters(generics.ListAPIView):
    permission_classes = [AllowAny]

    def get_queryset(self):

        sort = self.request.query_params.get("sort", None)
        group = self.request.query_params.get("group", None)
        location = self.request.query_params.get("location", None)
        category = self.request.query_params.get("category", None)
        supplier = self.request.query_params.get("supplier", None)
        name = self.request.query_params.get("name", None)
        isapproved = self.request.query_params.get("isapproved", None)

        print(sort)
        print(group)
        print(location)
        print(category)
        print(supplier)
        print(name)
        print(isapproved)

        queryset = Inventory.objects.all()

        if isapproved is not None and isapproved=="false":
            try:
                if len(queryset) != 0:
                    queryset = queryset.filter(IsApproved=False)
                    print("Filtered Group " + str(len(queryset)))
            except Exception as e:
                print(e)
        else:
            try:
                if len(queryset) != 0:
                    queryset = queryset.filter(IsApproved=True)
                    print("Filtered Group " + str(len(queryset)))
            except Exception as e:
                print(e)

        if group is not None:
            try:
                if len(queryset) != 0:
                    queryset = queryset.filter(Group__id=group)
                    print("Filtered Group " + str(len(queryset)))
            except Exception as e:
                print(e)

        if location is not None:
            try:
                if len(queryset) != 0:
                    queryset = queryset.filter(Location__id=location)
                    print("Filtered Location " + str(len(queryset)))
            except Exception as e:
                print(e)

        if category is not None:
            try:
                if len(queryset) != 0:
                    queryset = queryset.filter(Category__id=category)
                    print("Filtered Supplier " + str(len(queryset)))
            except Exception as e:
                print(e)

        if supplier is not None:
            try:
                if len(queryset) != 0:
                    queryset = queryset.filter(Supplier__id=supplier)
                    print("Filtered Supplier " + str(len(queryset)))
            except Exception as e:
                print(e)

        if name is not None:
            try:
                if len(queryset) != 0:
                    queryset = queryset.filter(
                        Q(ItemName__icontains=name) | Q(ItemKnownAs__icontains=name)
                    )
            except Exception as e:
                print(e)

        if sort == "asc":
            if len(queryset) != 0:
                queryset = queryset.order_by("ItemName")
        elif sort == "dec":
            if len(queryset) != 0:
                queryset = queryset.order_by("-ItemName")

        return queryset

    def get(self, request):

        # Users should be authenticated
        if not (request.user and request.user.is_authenticated):
            return Response(
                {
                    "success": False,
                    "message": "Authentication failed",
                    "data": {},
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            inventory_objects = list(self.get_queryset())

            if inventory_objects is not None and len(inventory_objects) != 0:
                serializer = InventorySerializer(inventory_objects, many=True)

                return Response(
                    {
                        "success": True,
                        "message": "List of the inventory Products",
                        "data": {
                            "count": len(serializer.data),
                            "list": serializer.data,
                        },
                    },
                    status=status.HTTP_200_OK,
                )

            return Response(
                {
                    "success": True,
                    "message": "No Products Present",
                    "data": {
                        "count": 0,
                        "list" : {},
                    },
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            print(e)


class GetUnApprovedProducts(generics.ListAPIView):
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Inventory.objects.filter(IsApproved=False)
        # make search by lower
        search_by = self.request.query_params.get("search_by", "")
        search = self.request.query_params.get("search", "")

        if (search_by == None or search_by == "") and (search == None or search == ""):
            return queryset

        search_by = search_by.lower()
        if search_by == "groups":
            try:
                queryset = queryset.filter(Group__id=search)
            except Exception as e:
                print(e)

        elif search_by == "categories":
            try:
                queryset = queryset.filter(Category__id=search)
            except Exception as e:
                print(e)

        elif search_by == "locations":
            try:
                queryset = queryset.filter(Location__id=search)
            except Exception as e:
                print(e)

        elif search_by == "status":
            try:
                if search == 0:
                    status = "inactive"
                else:
                    status = "active"

                queryset = queryset.filter(ItemStatus=status)
            except Exception as e:
                print(e)

        elif search_by == "name":
            queryset = queryset.filter(
                Q(ItemName__icontains=search) | Q(ItemKnownAs__icontains=search)
            )

        elif search_by == "suppliers":
            try:
                queryset = queryset.filter(Supplier__id=search)
            except Exception as e:
                print(e)

        return queryset

    def get(self, request):

        # Users should be authenticated
        if not (request.user and request.user.is_authenticated):
            return Response(
                {
                    "success": False,
                    "message": "Authentication failed",
                    "data": {},
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            inventory_objects = self.get_queryset()
            # inventory_objects = Inventory.objects.all()

            if inventory_objects is not None:
                serializer = InventorySerializer(inventory_objects, many=True)

                return Response(
                    {
                        "success": True,
                        "message": "List of the inventory Products",
                        "data": {
                            "count": len(serializer.data),
                            "list": serializer.data,
                        },
                    },
                    status=status.HTTP_200_OK,
                )

            return Response(
                {
                    "success": False,
                    "message": "No Products Present",
                    "data": {},
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception as e:
            print(e)


class PostApproveInventory(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        # Users should be authenticated
        if not (request.user and request.user.is_authenticated):
            return Response(
                {
                    "success": False,
                    "message": "Authentication failed",
                    "data": {},
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        product_id = request.data.get("product_id", None)
        user_id = request.data.get("user_id", None)
        user = request.user

        if not request.user.is_admin:
            return Response(
                {
                    "success": False,
                    "message": "User doesn't have admin privileges",
                    "data": {},
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            product = Inventory.objects.get(id=product_id)
        except Inventory.DoesNotExist:
            product = None

        if product is None:
            return Response(
                {
                    "success": False,
                    "message": "Wrong product id passed.",
                    "data": {},
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if product.IsApproved == True:
            return Response(
                {
                    "success": False,
                    "message": "Product is already apprpved.",
                    "data": {},
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        product.IsApproved = True
        product.RequestApprovedBy = user
        product.RequestApprovedDate = datetime.now()
        product.save()

        return Response(
            {
                "success": True,
                "message": f"Product {product.ItemName} with id {product.id} is approved",
                "data": "",
            },
            status=status.HTTP_200_OK,
        )


class GetProductDetails(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):

        # Users should be authenticated
        if not (request.user and request.user.is_authenticated):
            return Response(
                {
                    "success": False,
                    "message": "Authentication failed",
                    "data": {},
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            inventory_obj = Inventory.objects.get(id=pk)
            if inventory_obj is not None:
                serializer = InventorySerializer(inventory_obj)

                return Response(
                    {
                        "success": True,
                        "message": "Inventory Product Details",
                        "data": {"count": 1, "list": serializer.data},
                    },
                    status=status.HTTP_200_OK,
                )

            return Response(
                {
                    "success": False,
                    "message": "No Product exists with the provided id",
                    "data": {},
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception as e:
            print(e)


class GetProductsSortedByLocations(APIView):
    permission_classes = [AllowAny]

    def get(self, request):

        # context = {}
        context_list = []
        # Users should be authenticated
        if not (request.user and request.user.is_authenticated):
            return Response(
                {
                    "success": False,
                    "message": "Authentication failed",
                    "data": {},
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        sort = request.GET.get("sort", "")

        location_objs = Location.objects.all()
        # inventories_objs = []

        if location_objs is not None or location_objs.len != 0:
            for location in location_objs:
                qs = []
                qs = Inventory.objects.filter(IsApproved=True, Location=location)
                if sort == "asc":
                    qs.order_by("ItemName")
                else:
                    qs.order_by("-ItemName")

                qs_serializer = InventorySerializer(qs, many=True)
                temp_dict = {}
                temp_dict["location_name"] = location.name
                temp_dict["location_id"] = location.id
                temp_dict["inventory_count"] = len(qs_serializer.data)
                temp_dict["inventory_list"] = qs_serializer.data
                context_list.append(temp_dict)

            return Response(
                {
                    "success": True,
                    "message": "Inventory per location",
                    "data": {"count": len(context_list), "list": context_list},
                },
                status=200,
            )

        return Response(
            {
                "success": False,
                "message": "No Locations In Database",
                "data": [],
            },
            status=400,
        )


class DeleteInventory(APIView):
    permission_classes = [AllowAny]

    def post(self, request, pk):
        if not (request.user and request.user.is_authenticated):
            return Response(
                {
                    "success": False,
                    "message": "Authentication failed",
                    "data": {},
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            item = Inventory.objects.get(id=pk)
        except Inventory.DoesNotExist:
            item = None

        if item is not None:
            item.delete()
            return Response(
                {
                    "success": True,
                    "message": "Inventory Deleted",
                    "data": {},
                },
                status=200,
            )

        return Response(
            {
                "success": False,
                "message": "No Inventory with the given id exists",
                "data": {},
            },
            status=400,
        )


class InventoryReportList(generics.ListAPIView):
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Inventory.objects.filter(IsApproved=True)
        search_by = self.request.query_params.get("search_by", "")
        search = self.request.query_params.get("search", "")

        if (search_by == None or search_by == "") and (search == None or search == ""):
            return queryset

        search_by = search_by.lower()
        if search_by == "groups":
            try:
                queryset = queryset.filter(Group__id=search)
            except Exception as e:
                print(e)

        elif search_by == "categories":
            try:
                queryset = queryset.filter(Category__id=search)
            except Exception as e:
                print(e)

        elif search_by == "locations":
            try:
                queryset = queryset.filter(Location__id=search)
            except Exception as e:
                print(e)

        elif search_by == "status":
            try:
                if search == 0:
                    status = "inactive"
                else:
                    status = "active"

                queryset = queryset.filter(ItemStatus=status)
            except Exception as e:
                print(e)

        elif search_by == "name":
            queryset = queryset.filter(
                Q(ItemName__icontains=search) | Q(ItemKnownAs__icontains=search)
            )

        elif search_by == "suppliers":
            try:
                queryset = queryset.filter(Supplier__id=search)
            except Exception as e:
                print(e)

        return queryset

    def get(self, request):
        # Users should be authenticated
        if not (request.user and request.user.is_authenticated):
            return Response(
                {
                    "success": False,
                    "message": "Authentication failed",
                    "data": {},
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        data = []

        objs = self.get_queryset()
        objs_list = list(objs)

        for index in range(0, len(objs_list)):
            ist_objs = InventoryStockTransaction.objects.filter(
                IDRecord=objs_list[index].id
            )
            ist_objs_in = ist_objs.filter(
                IDRecord=objs_list[index].id, Type="In"
            ).order_by("-DateTransaction")
            # print(f"LENGTH ist_objs_in: {len(ist_objs_in)}")
            stock_in_hand = 0
            if ist_objs is not None:
                for i in ist_objs:
                    if i.Type == "In":
                        stock_in_hand += i.Units if (i.Units is not None) else 0
                    else:
                        stock_in_hand -= i.Units if (i.Units is not None) else 0

            if len(ist_objs_in) != 0:
                data_item = {
                    "id": objs_list[index].id,
                    "currentDate": datetime.now(),
                    "RecordsFound": 1,
                    "ItemKnownAs": objs_list[index].ItemKnownAs,
                    "ItemType": objs_list[index].ItemType,
                    "Group": objs_list[index].Group,
                    "Location": objs_list[index].Location,
                    "ReorderLevel": objs_list[index].ReorderLevel,
                    "StockUnitPrice": objs_list[index].StockUnitPrice,
                    "UnitsMeasure": ist_objs_in[0].UnitsMeasure,
                    "UnitsOnHand": stock_in_hand,
                    "LastOrdered": ist_objs_in[0].DateTransaction,
                }
            else:
                data_item = {
                    "id": objs_list[index].id,
                    "currentDate": datetime.now(),
                    "RecordsFound": 1,
                    "ItemKnownAs": objs_list[index].ItemKnownAs,
                    "ItemType": objs_list[index].ItemType,
                    "Group": objs_list[index].Group,
                    "Location": objs_list[index].Location,
                    "ReorderLevel": objs_list[index].ReorderLevel,
                    "StockUnitPrice": objs_list[index].StockUnitPrice,
                    "UnitsMeasure": "",
                    "UnitsOnHand": stock_in_hand,
                    "LastOrdered": "",
                }

            data.append(data_item)

        serializer = InventoryReportSerializer(data, many=True)

        return Response(
            {
                "success": True,
                "message": "Report for the list of products",
                "data": {"count": len(serializer.data), "data": serializer.data},
            },
            status=200,
        )


class InventoryReportDetails(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        # Users should be authenticated
        if not (request.user and request.user.is_authenticated):
            return Response(
                {
                    "success": False,
                    "message": "Authentication failed",
                    "data": {},
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            obj = Inventory.objects.get(id=pk)
        except Inventory.DoesNotExist:
            obj = None

        if obj is None:
            return Response(
                {
                    "success": False,
                    "message": "No product with the provided id exists",
                    "data": {},
                },
                status=404,
            )

        ist_objs = InventoryStockTransaction.objects.filter(IDRecord=obj.id)

        if len(ist_objs) != 0:
            ist_objs_in = ist_objs.filter(IDRecord=obj.id, Type="In").order_by(
                "-DateTransaction"
            )
            stock_in_hand = 0

            if ist_objs is not None:
                for i in ist_objs:
                    if i.Type == "In":
                        stock_in_hand += i.Units if (i.Units is not None) else 0
                    else:
                        stock_in_hand -= i.Units if (i.Units is not None) else 0

            data = {
                "id": obj.id,
                "currentDate": datetime.now(),
                "RecordsFound": 1,
                "ItemKnownAs": obj.ItemKnownAs,
                "ItemType": obj.ItemType,
                "Group": obj.Group,
                "Location": obj.Location,
                "ReorderLevel": obj.ReorderLevel,
                "StockUnitPrice": obj.StockUnitPrice,
                "UnitsMeasure": ist_objs_in[0].UnitsMeasure,
                "UnitsOnHand": stock_in_hand,
                "LastOrdered": ist_objs_in[0].DateTransaction,
            }

        else:
            data = {
                "id": obj.id,
                "currentDate": datetime.now(),
                "RecordsFound": 1,
                "ItemKnownAs": obj.ItemKnownAs,
                "ItemType": obj.ItemType,
                "Group": obj.Group,
                "Location": obj.Location,
                "ReorderLevel": obj.ReorderLevel,
                "StockUnitPrice": obj.StockUnitPrice,
                "UnitsMeasure": "",
                "UnitsOnHand": 0,
                "LastOrdered": "",
            }

        serializer = InventoryReportSerializer(data)

        return Response(
            {
                "success": True,
                "message": "Report for the object",
                "data": {"data": serializer.data},
            },
            status=200,
        )




# Inventory Stock Transactin API's

class GetInventoryStockTransactionForProduct(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id):
        # Users should be authenticated
        if not (request.user and request.user.is_authenticated):
            return Response(
                {
                    "success": False,
                    "message": "Authentication failed",
                    "data": {},
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            inventory_st_objects = InventoryStockTransaction.objects.filter(
                IDRecord=id
            ).order_by("-DateTransaction")

            if inventory_st_objects is not None:
                serializer = InventoryStockTransactionSerializer(
                    inventory_st_objects, many=True
                )

                return Response(
                    {
                        "success": True,
                        "message": "List of the inventory stock transactions",
                        "data": {
                            "count": len(serializer.data),
                            "list": serializer.data,
                        },
                    },
                    status=status.HTTP_200_OK,
                )

            return Response(
                {
                    "success": False,
                    "message": "Not able to find any inventory transactions",
                    "data": {},
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception as e:
            print(e)


class PostInventoryStockTransactionIn(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Users should be authenticated
        if not (request.user and request.user.is_authenticated):
            return Response(
                {
                    "success": False,
                    "message": "Authentication failed",
                    "data": {},
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        units = request.data.get("units")
        # amount = request.data.get("amount")
        product_id = request.data.get("product_id")
        unit_measure = request.data.get("unit_measure")
        date = request.data.get("date", None)
        user = request.user
        lot_number = request.data.get("lot_number")
        description = request.data.get("description", "")

        print(f"Um : {unit_measure}")
        print(f"Description : {description}")
        print(f"Date : {date}")


        try:
            unit_measure_obj = UnitsMeasure.objects.get(id=unit_measure)
        except UnitsMeasure.DoesNotExist:
            unit_measure_obj = None

        try:
            product = Inventory.objects.get(id=product_id, IsApproved=True)
        except Inventory.DoesNotExist:
            product = None

        if product is None:
            return Response(
                {
                    "success": False,
                    "message": "Wrong product id passed or product is not yet approved",
                    "data": {},
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if description == "":
            description = product.ItemName
        if date == None:
            date = datetime.now()

        inventory_st = InventoryStockTransaction.objects.create(
            Description=description,
            IDRecord=product,
            Type="In",
            TypeId=1,  # 1:in, 2:out
            Units=units,
            UnitsMeasure=unit_measure_obj,
            LotNumber=lot_number,
            DateTransaction=date,
        )

        inventory_st.IDItem = inventory_st.id
        inventory_st.DateTransaction = datetime.now()

        ist_objs = InventoryStockTransaction.objects.filter(IDRecord=product.id)
        # stock_in_hand = 0
        # # print("List of Objs")
        # # print(ist_objs)
        # # print(ist_objs[1].Units if (ist_objs[1].Units is not None) else 0)

        # if ist_objs is not None:
        #     for i in ist_objs:
        #         if i.Type == "In":
        #             stock_in_hand += i.Units if (i.Units is not None) else 0
        #         else:
        #             stock_in_hand -= i.Units if (i.Units is not None) else 0

        # print("out of if loop")
        # stock_in_hand += float(units)

        # inventory_st.UnitsMeasure = stock_in_hand
        # inventory_st.save()
        # serializer = InventoryStockTransactionSerializer(inventory_st)

        return Response(
            {
                "success": True,
                "message": "Successful In operation",
                "data": {},
                # "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class PostInventoryStockTransactionOut(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Users should be authenticated
        if not (request.user and request.user.is_authenticated):
            return Response(
                {
                    "success": False,
                    "message": "Authentication failed",
                    "data": {},
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        units = request.data.get("units") 
        product_id = request.data.get("product_id")
        unit_measure = request.data.get("unit_measure")
        date = request.data.get("date", None)
        user = request.user
        lot_number = request.data.get("lot_number")
        description = request.data.get("description", "")

        print(f"Um : {unit_measure}")
        print(f"Description : {description}")
        print(f"Date : {date}")
        # print(f"{} : {}")

        try:
            unit_measure_obj = UnitsMeasure.objects.get(id=unit_measure)
        except UnitsMeasure.DoesNotExist:
            unit_measure_obj = None

        try:
            product = Inventory.objects.get(id=product_id, IsApproved=True)
        except Inventory.DoesNotExist:
            product = None

        if product is None:
            return Response(
                {
                    "success": False,
                    "message": "Wrong product id passed or product is not yet approved",
                    "data": {},
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if description == "":
            description = product.ItemName
        if date == None:
            date = datetime.now()

        inventory_st = InventoryStockTransaction.objects.create(
            Description=description,
            IDRecord=product,
            Type="Out",
            TypeId=2,  # 1:in, 2:out
            Units=units,
            UnitsMeasure=unit_measure_obj,
            LotNumber=lot_number,
            DateTransaction=date,
        )

        # inventory_st.IDItem = inventory_st.id
        # inventory_st.DateTransaction = datetime.now()

        # ist_objs = InventoryStockTransaction.objects.filter(IDRecord=product.id)

        # stock_in_hand = 0

        # if ist_objs is not None and len(ist_objs) != 0:
        #     for i in ist_objs:
        #         if i.Type == "In":
        #             stock_in_hand += i.Units if (i.Units is not None) else 0
        #         else:
        #             stock_in_hand -= i.Units if (i.Units is not None) else 0

        # stock_in_hand -= float(units)
        # inventory_st.UnitsMeasure = stock_in_hand
        # inventory_st.save()

        # serializer = InventoryStockTransactionSerializer(inventory_st)
        return Response(
            {
                "success": True,
                "message": "Successful Out operation",
                "data": {},
                # "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class PostInventoryStockTransaction(APIView):
    permission_classes = [AllowAny]

    def post(self, request, action, id):
        # Users should be authenticated
        if not (request.user and request.user.is_authenticated):
            return Response(
                {
                    "success": False,
                    "message": "Authentication failed",
                    "data": {},
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        if not (action == "in" or action == "out"):
            return Response(
                {
                    "success": False,
                    "message": "Action not supported",
                    "data": {},
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            product = Inventory.objects.get(id=id, IsApproved=True)
        except Inventory.DoesNotExist:
            product = None

        if product is None:
            return Response(
                {
                    "success": False,
                    "message": "Wrong product id passed or product not yet approved",
                    "data": {},
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if action == "in":
            inventory_st = InventoryStockTransaction.objects.create(
                Description=product.ItemName,
                IDRecord=product,
                Type="In",
            )

            inventory_st.save()
            serializer = InventoryStockTransactionSerializer(inventory_st)
            return Response(
                {
                    "success": True,
                    "message": "Successful In operation",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )

        if action == "out":
            inventory_st = InventoryStockTransaction.objects.create(
                Description=product.ItemName,
                IDRecord=product,
                Type="Out",
            )

            inventory_st.save()
            serializer = InventoryStockTransactionSerializer(inventory_st)
            return Response(
                {
                    "success": True,
                    "message": "Successful Out operation",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )


class DeleteStockTransactionRecord(APIView):
    permission_classes = [
        AllowAny,
    ]

    def post(self, request, pk):
        # Users should be authenticated
        if not (request.user and request.user.is_authenticated):
            return Response(
                {
                    "success": False,
                    "message": "Authentication failed",
                    "data": {},
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            item = InventoryStockTransaction.objects.get(id=pk)
        except InventoryStockTransaction.DoesNotExist:
            item = None

        if item is not None:
            item.delete()
            return Response(
                {
                    "success": True,
                    "message": "Stock Transaction Record Deleted",
                    "data": {},
                },
                status=200,
            )

        return Response(
            {
                "success": False,
                "message": "No Stock Transaction Record with the given id exists",
                "data": {},
            },
            status=400,
        )


class UpdateInventoryStockTransaction(APIView):
    permission_classes = [AllowAny]

    def post(self, request, pk):
        if not (request.user and request.user.is_authenticated):
            return Response(
                {
                    "success": False,
                    "message": "Authentication failed",
                    "data": {},
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            item = InventoryStockTransaction.objects.get(id=pk)
        except InventoryStockTransaction.DoesNotExist:
            item = None

        if item is not None:
            serializer = InventoryStockTransactionSerializer(instance=item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "success": True,
                        "message": "Inventory Stock Transaction Updated",
                        "data": serializer.data,
                    },
                    status=201,
                )

        return Response(
            {
                "success": False,
                "message": "No inventory stock transaction with the given id exists",
                "data": serializer.errors,
            },
            status=400,
        )



# Inventory SDS Records API's

class InventorySDSRecordList(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Users should be authenticated
        if not (request.user and request.user.is_authenticated):
            return Response(
                {
                    "success": False,
                    "message": "Authentication failed",
                    "data": {},
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = InventorySDSRecordSerializer(data=request.data)

        try:
            obj = InventorySDSRecord.objects.get(SDSNameURL=request.data["SDSNameURL"])
        except InventorySDSRecord.DoesNotExist:
            obj = None

        if obj is not None:
            return Response(
                {
                    "success": False,
                    "message": "A SDS Record with the same name already exists",
                    "data": {},
                },
                status=400,
            )

        if serializer.is_valid():
            serializer.save()

        return Response(
            {
                "success": True,
                "message": "SDS record successfully created",
                "data": serializer.data,
            },
            status=201,
        )

    def get(self, request):
        # Users should be authenticated
        if not (request.user and request.user.is_authenticated):
            return Response(
                {
                    "success": False,
                    "message": "Authentication failed",
                    "data": {},
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        objs = InventorySDSRecord.objects.all()
        serializer = InventorySDSRecordSerializer(objs, many=True)
        return Response(
            {
                "success": True,
                "message": "List of all SDS Records",
                "data": {"count": len(serializer.data), "data": serializer.data},
            },
            status=200,
        )


class InventorySDSRecordDetails(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        # Users should be authenticated
        if not (request.user and request.user.is_authenticated):
            return Response(
                {
                    "success": False,
                    "message": "Authentication failed",
                    "data": {},
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            obj = InventorySDSRecord.objects.get(id=pk)
        except InventorySDSRecord.DoesNotExist:
            obj = None

        if obj is None:
            return Response(
                {
                    "success": False,
                    "message": "No SDS Record with the provided key exists",
                    "data": {},
                },
                status=400,
            )

        serializer = InventorySDSRecordSerializer(obj)

        return Response(
            {
                "success": True,
                "message": "List of all SDS Records",
                "data": {"count": len(serializer.data), "data": serializer.data},
            },
            status=200,
        )


class GetSDSRecordDetailsFromProductId(APIView):
    permission_classes = [AllowAny]

    def get(self, request, product_id):
        # Users should be authenticated
        if not (request.user and request.user.is_authenticated):
            return Response(
                {
                    "success": False,
                    "message": "Authentication failed",
                    "data": {},
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            obj = InventorySDSRecord.objects.get(IDRecord=product_id)
        except InventorySDSRecord.DoesNotExist:
            obj = None

        if obj is None:
            return Response(
                {
                    "success": False,
                    "message": "No SDS Record for the selected product exists",
                    "data": {},
                },
                status=400,
            )

        serializer = InventorySDSRecordSerializer(obj)

        return Response(
            {
                "success": True,
                "message": "SDS record for the selected product",
                "data": serializer.data,
            },
            status=200,
        )


class UpdateSDSRecord(APIView):
    permission_classes = [AllowAny]

    def post(self, request, pk):
        if not (request.user and request.user.is_authenticated):
            return Response(
                {
                    "success": False,
                    "message": "Authentication failed",
                    "data": {},
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            item = InventorySDSRecord.objects.get(id=pk)
        except InventorySDSRecord.DoesNotExist:
            item = None

        if item is not None:
            serializer = InventorySDSRecordSerializer(instance=item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                print(serializer.data.get("id"))
                return Response(
                    {
                        "success": True,
                        "message": "Inventory SDS Record Updated",
                        "data": {},
                        # "data": serializer.data,
                    },
                    status=201,
                )

        return Response(
            {
                "success": False,
                "message": "No invenentory SDS RECORD with the given id exists",
                "data": serializer.errors,
            },
            status=400,
        )


class CreateSDSRecord(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        if not (request.user and request.user.is_authenticated):
            return Response(
                {
                    "success": False,
                    "message": "Authentication failed",
                    "data": {},
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = InventorySDSRecordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "SDS Record created",
                    "data": serializer.data,
                },
                status=201,
            )

        return Response(
            {
                "success": False,
                "message": "Error occured while creating SDS Record Data",
                "data": serializer.errors,
            },
            status=400,
        )

#   ------------------------------------------------------------------------------------------

# NotUsing
class CreateInventoryNew(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Users should be authenticated
        if not (request.user and request.user.is_authenticated):
            return Response(
                {
                    "success": False,
                    "message": "Authentication failed",
                    "data": {},
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = CreateInventorySerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "Product created",
                    "data": {},
                },
                status=201,
            )

        return Response(
            {
                "success": False,
                "message": "Error occured",
                "data": serializer.errors,
            },
            status=400,
        )


# Not Using
class InvnetoryCreateUpdateGet(
    mixins.RetrieveModelMixin, mixins.CreateModelMixin, GenericAPIView
):

    serializer_class = InventorySerializer
    queryset = Inventory.objects.all()

    def get(self, request, *args, **kwargs):
        data = self.retrieve(request, *args, **kwargs)
        print(data)
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


# Not using
class InventoryList(generics.ListAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializerNewWay
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = InventoryFilter

