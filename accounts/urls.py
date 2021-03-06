from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("signup", views.signup, name="signup"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("profile", views.profile, name="profile"),
    path("orders", views.orders, name="orders"),
    path("orders/<id>", views.order_details, name="order-detail"),
]

