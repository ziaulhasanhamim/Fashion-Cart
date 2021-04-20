from django.contrib.auth.models import User
from django.db import models
from core.models.shipping import ShippingAndBilling
from core.models.order_status_choices import OrderStatusChoices


class Customer(models.Model):
    user: User = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self) -> int:
        return self.user.username

    def get_placed_order_count(self) -> int:
        return self.order_set.filter(date_ordered__isnull=False).count()

    def get_cancelled_order_count(self) -> int:
        return self.order_set.filter(status=OrderStatusChoices.CANCELLED).count()
