from django.db import models

class OrderStatusChoices(models.IntegerChoices):
    NOT_ORDERED = 0, "Not Ordered"
    PENDING = 1, "Pending"
    PROCESSING = 2, "Processing"
    DELIVERED = 3, "Delivered"
    CANCELLED = -1, "Cancelled"
    