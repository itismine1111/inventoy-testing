from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, "app_frontend/ctemplates/index.html")


def login(request):
    return render(request, "app_frontend/login.html")


def forgot_password(request):
    return render(request, "app_frontend/forgot_password.html")


def confirm_otp(request):
    return render(request, "app_frontend/confirm_otp.html")


def reset_password(request):
    return render(request, "app_frontend/reset_password.html")


def enter_new_product(request):
    return render(request, "app_frontend/enter_new_product.html")


def add_groups_form(request):
    return render(request, "app_frontend/add_groups_form.html")


def add_locations_form(request):
    return render(request, "app_frontend/add_locations_form.html")


def add_categories_form(request):
    return render(request, "app_frontend/add_categories_form.html")


def add_suppliers_form(request):
    return render(request, "app_frontend/add_suppliers_form.html")


def add_units_measure_form(request):
    return render(request, "app_frontend/add_units_measure_form.html")


def list_products_page(request):
    return render(request, "app_frontend/list_products_page.html")