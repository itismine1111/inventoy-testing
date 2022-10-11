from django.urls import URLPattern, path
from knox import views as knox_views

from .views import (
    TempCreate
)

app_name = "app_temp"

urlpatterns = [
    path("temp-create/", TempCreate.as_view(), name="temp-create"),

]
