from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from datetime import datetime
from django.db.models import Avg
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.shortcuts import reverse
from core.models.category import Category

gender_choices = [
    ("men", "Men"),
    ("women", "Women"),
    ("both", "Both")
]

class Product(models.Model):
    title = models.CharField(max_length=500)
    summary = models.TextField(max_length=1000)
    description = RichTextUploadingField(null=True, blank=True)
    thumbnail = models.ImageField(upload_to="product_thumbnails/")
    price = models.DecimalField(max_digits=12, decimal_places=2)
    discount_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, related_name="products", blank=True)
    for_gender = models.CharField(max_length=10, choices=gender_choices, default="men")
    sold = models.IntegerField(default=0)
    url = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.url == None:
            slug = slugify(self.title)
            while Product.objects.filter(url=slug).exists():
                slug += f"-{self.id}"
            self.url = slug
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title

    def get_price(self) -> float:
        if self.discount_price:
            return self.discount_price
        return self.price

    def get_absolute_url(self):
        return reverse("core:product-detail", kwargs={"slug": self.url})

    def get_discount_percent(self):
        if self.discount_price != None:
            return int((self.price - self.discount_price) / self.price * 100)
        return 0

    @property
    def avg_rating(self) -> float:
        return self.reviews.all().aggregate(avg=Avg("rating"))["avg"] if self.reviews.count() > 0 else 0

    def get_avg_stars(self) -> str:
        stars = ""
        for i in range(0, int(self.avg_rating)):
            stars += """<i class="fas fa-star"></i>"""
        far_star = 5-(int(self.avg_rating))
        if (self.avg_rating - int(self.avg_rating)) != 0:
            stars += """<i class="fas fa-star-half-alt"></i>"""
            far_star -= 1
        for i in range(0, far_star):
            stars += """<i class="far fa-star"></i>"""
        return stars


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="product_images/")

    def url(self) -> str:
        return self.image.url

