from django.db import models


class PaymentOptionChoies(models.IntegerChoices):
    BKASH = 1, "Bkash",
    CASH_ON_DELIVERY = 2, "Cash On Delivery"


class ShippingAndBilling(models.Model):
    name = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street_address = models.CharField(max_length=500)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    payment_option = models.IntegerField(default=PaymentOptionChoies.BKASH, choices=PaymentOptionChoies.choices)
    bkash_number = models.CharField(max_length=20, null=True, blank=True)
    shipping_charge = models.IntegerField(default=0)
