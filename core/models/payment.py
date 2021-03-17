from django.db import models
from django.db.models import Avg
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.shortcuts import reverse
from datetime import datetime
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.exceptions import ValidationError


class PaymentOptionChoies(models.IntegerChoices):
    BKASH = 1, "Bkash",
    CASH_ON_DELIVERY = 2, "Cash On Delivery"


class Payment(models.Model):
    option = models.IntegerField(default=PaymentOptionChoies.CASH_ON_DELIVERY, choices=PaymentOptionChoies.choices)
    number = models.CharField(max_length=20)
