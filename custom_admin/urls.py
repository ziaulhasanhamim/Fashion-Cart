from django.urls import path
from . import views

app_name = "custom_admin"

urlpatterns = [
    path("orders", views.orders, name="orders"),
    path("orders/manage/<int:id>", views.manage_orders, name="manage_orders")
]
