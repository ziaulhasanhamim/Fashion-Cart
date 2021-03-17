from django.db import models

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
