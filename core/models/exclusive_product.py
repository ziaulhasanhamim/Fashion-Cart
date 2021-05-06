from django.db import models
from core.models import Product
from datetime import datetime


class ExclusiveProduct(models.Model):
    product: Product = models.OneToOneField(Product, on_delete=models.CASCADE)
    available_till: datetime = models.DateTimeField()
