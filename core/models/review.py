from django.db import models
from django.db.models import Avg
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.shortcuts import reverse
from datetime import datetime
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.exceptions import ValidationError
from core.models.product import Product
from core.models.customer import Customer


RATINGS_CHOICES = (
    (1, '1'),
    (1.5, '1.5'),
    (2.5, '2.5'),
    (3, '3'),
    (3.5, '3.5'),
    (4, '4'),
    (4.5, '4.5'),
    (5, '5')
)


class Review(models.Model):
    rating = models.FloatField(choices=RATINGS_CHOICES)
    user: Customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="reviews")
    message = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    timestamp = models.DateTimeField(auto_now_add=True)

    def get_stars(self) -> str:
        stars = ""
        for i in range(0, int(self.rating)):
            stars += """<i class="fas fa-star"></i>"""
        far_star = 5-(int(self.rating))
        if (self.rating - int(self.rating)) != 0:
            stars += """<i class="fas fa-star-half-alt"></i>"""
            far_star -= 1
        for i in range(0, far_star):
            stars += """<i class="far fa-star"></i>"""
        return stars

