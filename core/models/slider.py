from django.db import models
from django.db.models import Avg
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.shortcuts import reverse
from datetime import datetime
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.exceptions import ValidationError


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

