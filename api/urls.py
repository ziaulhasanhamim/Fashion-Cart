from django.urls import path
from . import views

app_name = "api"

urlpatterns = [
    path("cart", views.cart, name="cart"),
    path("products", views.product_list, name="products")
]
