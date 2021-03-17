from django.db import models
from django.db.models import Avg
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.shortcuts import reverse
from datetime import datetime
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.exceptions import ValidationError
from core.models.product import Product
from core.models.payment import Payment


class OrderStatusChoices(models.IntegerChoices):
    NOT_ORDERED = 0, "Not Ordered"
    PENDING = 1, "Pending"
    PROCESSING = 2, "Processing"
    DELIVERED = 3, "Delivered"
    CANCELLED = -1, "Cancelled"


class Order(models.Model):
    user: User = models.ForeignKey(User, on_delete=models.CASCADE)
    date_ordered: datetime = models.DateTimeField(null=True, blank=True)
    date_delivered: datetime = models.DateTimeField(null=True, blank=True)
    cancellion_reason: str = models.CharField(max_length=500, null=True, blank=True)
    status = models.IntegerField(default=OrderStatusChoices.NOT_ORDERED, choices=OrderStatusChoices.choices)
    payment = models.OneToOneField(Payment, on_delete=models.SET_NULL, null=True, blank=True)

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
