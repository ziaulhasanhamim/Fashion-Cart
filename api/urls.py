from django.urls import path
from . import views

app_name = "api"

urlpatterns = [
    path("cart", views.cart, name="cart")
]
