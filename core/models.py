from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

category_gender_choices = [
    ("men", "Men"),
    ("women", "Women"),
    ("none", "None")
]

class Category(models.Model):
    name: str = models.CharField(max_length=50, unique=True)
    image = models.ImageField(upload_to="category_images/", null=True, blank=True)
    featured_in = models.CharField(max_length=10, choices=category_gender_choices, default="none")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categories"


gender_choices = [
    ("men", "Men"),
    ("women", "Women")
]

class Product(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to="product_thumbnails/")
    price = models.DecimalField(max_digits=12, decimal_places=2)
    discount_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True);
    categories = models.ManyToManyField(Category, related_name="products", blank=True)
    for_gender = models.CharField(max_length=10, choices=gender_choices, default="men")
    sold = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="product_images/")


class Order(models.Model):
    user: User = models.ForeignKey(User, on_delete=models.CASCADE)
    date_ordered: datetime = models.DateTimeField(null=True, blank=True)
    date_delivered: datetime = models.DateTimeField(null=True, blank=True)


class OrderItem(models.Model):
    order: Order = models.ForeignKey(Order, on_delete=models.CASCADE, name="order_items");
    product: Product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order_items")
    quantity: int = models.IntegerField(default=1)
