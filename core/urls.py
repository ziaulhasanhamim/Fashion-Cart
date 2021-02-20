from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.index, name="index"),
    path("cart", views.cart, name="cart"),
    path("cart_items", views.cart_items, name="cart_items"),
    path("product/<slug>", views.product_detail, name="product-detail"),
    path("update_reviews", views.update_reviews, name="update-reviews")
]
