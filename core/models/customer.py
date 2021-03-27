from django.contrib.auth.models import User
from django.db import models
from core.models.shipping import ShippingAndBilling


class Customer(models.Model):
    user: User = models.OneToOneField(User, on_delete=models.CASCADE)
    default_shipping = models.ForeignKey(ShippingAndBilling, null=True, blank=True, on_delete=models.SET_NULL)
