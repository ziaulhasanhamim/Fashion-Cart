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

    def get_price(self) -> float:
        if self.discount_price:
            return self.discount_price
        return self.price


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="product_images/")


class Order(models.Model):
    user: User = models.ForeignKey(User, on_delete=models.CASCADE)
    date_ordered: datetime = models.DateTimeField(null=True, blank=True)
    date_delivered: datetime = models.DateTimeField(null=True, blank=True)

    @property
    def items_count(self):
        count = 0
        for item in self.order_items.all():
            assert isinstance(item, OrderItem)
            count += item.quantity
        return count

    @property
    def total_price(self) -> float:
        total = 0;
        for item in self.order_items.all().select_related("product"):
            total += item.get_net_price()
        return total

    def get_items(self):
        return self.order_items.all().select_related("product")


class OrderItem(models.Model):
    order: Order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items", null=True);
    product: Product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order_items")
    quantity: int = models.IntegerField(default=1)

    def get_net_price(self) -> float:
        return self.product.get_price() * self.quantity


class Slider(models.Model):
    primary_tagline = models.CharField(max_length=200)
    secondary_tagline = models.CharField(max_length=100, null=True, blank=True)
    important_text = models.CharField(max_length=300, null=True, blank=True)
    starting_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    link = models.CharField(max_length=500, null=True, blank=True)
    link_text = models.CharField(max_length=30, null=True, blank=True)
    image = models.ImageField(upload_to="sliders/")
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.primary_tagline
    
    @property
    def is_link(self):
        if self.link != None and self.link_text != None:
            return True
        return False
