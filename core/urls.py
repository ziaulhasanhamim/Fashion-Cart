from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.index, name="index"),
    path("cart", views.cart, name="cart"),
    path("product/<slug>", views.product_detail, name="product-detail"),
    path("update_reviews", views.update_reviews, name="update-reviews"),
    path("products", views.products, name="products"),
    path("products/category/<category>/gender/<gender>", views.category_products, name="products")
]
