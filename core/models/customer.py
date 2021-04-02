from django.contrib.auth.models import User
from django.db import models
from core.models.shipping import ShippingAndBilling


class Customer(models.Model):
    user: User = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
