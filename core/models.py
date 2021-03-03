from django.db import models
from django.db.models import Avg
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.shortcuts import reverse
from datetime import datetime
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.exceptions import ValidationError

category_gender_choices = [
    ("men", "Men"),
    ("women", "Women"),
    ("none", "None")
]


class Category(models.Model):
    name: str = models.CharField(max_length=50, unique=True)
    image = models.ImageField(upload_to="category_images/", null=True, blank=True)
    featured_in = models.CharField(max_length=10, choices=category_gender_choices, default="none")

    def clean(self):
        if Category.objects.filter(name__iexact=self.name):
            raise ValidationError("Name Should Be Unique")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categories"


gender_choices = [
    ("men", "Men"),
    ("women", "Women")
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


class Order(models.Model):
    user: User = models.ForeignKey(User, on_delete=models.CASCADE)
    date_ordered: datetime = models.DateTimeField(null=True, blank=True)
    date_delivered: datetime = models.DateTimeField(null=True, blank=True)

    @property
    def items_count(self):
        count = 0
        for item in self.order_items.all():
            assert isinstance(item, OrderItem)
            count += item.quantity
        return count

    @property
    def total_price(self) -> float:
        total = 0;
        for item in self.order_items.all().select_related("product"):
            total += item.get_net_price()
        return total

    def get_items(self):
        return self.order_items.all().select_related("product")


class OrderItem(models.Model):
    order: Order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items", null=True);
    product: Product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order_items")
    quantity: int = models.IntegerField(default=1)

    def get_net_price(self) -> float:
        return self.product.get_price() * self.quantity


class Slider(models.Model):
    primary_tagline = models.CharField(max_length=200)
    secondary_tagline = models.CharField(max_length=100, null=True, blank=True)
    important_text = models.CharField(max_length=300, null=True, blank=True)
    starting_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    link = models.CharField(max_length=500, null=True, blank=True)
    link_text = models.CharField(max_length=30, null=True, blank=True)
    image = models.ImageField(upload_to="sliders/")
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.primary_tagline
    
    @property
    def is_link(self):
        if self.link != None and self.link_text != None:
            return True
        return False


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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
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
