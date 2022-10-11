from django.urls import path
from .views import (
    forgot_password,
    index,
    login,
    forgot_password,
    confirm_otp,
    reset_password,
    enter_new_product,
    add_groups_form,
    add_locations_form,
    add_categories_form,
    add_suppliers_form,
    list_products_page,
    add_units_measure_form,
)

app_name = "app_frontend"


urlpatterns = [
    path("", index, name="index"),
    path("login/", login, name="login"),
    path("forgot-password/", forgot_password, name="forgot-password"),
    path("confirm-otp/", confirm_otp, name="confirm-otp"),
    path("reset-password/", reset_password, name="reset-password"),
    path("new-product/", enter_new_product, name="new-product"),
    path("add-groups-form/", add_groups_form, name="add-groups-form"),
    path("add-locations-form/", add_locations_form, name="add-locations-form"),
    path("add-categories-form/", add_categories_form, name="add-categories-form"),
    path("add-suppliers-form/", add_suppliers_form, name="add-suppliers-form"),
    path("add-units-measure-form/", add_units_measure_form, name="add-units-measure-form"),
    path("list-page/", list_products_page, name="list-page"),
]
