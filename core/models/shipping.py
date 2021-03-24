from django.db import models


class PaymentOptionChoies(models.IntegerChoices):
    BKASH = 1, "Bkash",
    CASH_ON_DELIVERY = 2, "Cash On Delivery"


class ShippingAndPayment(models.Model):
    city = models.CharField(max_length=100)
    full_address = models.CharField(max_length=500)
    zip_code = models.IntegerField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    payment_option = models.IntegerField(default=PaymentOptionChoies.BKASH, choices=PaymentOptionChoies.choices)
    bkash_number = models.CharField(max_length=20, null=True, blank=True)
