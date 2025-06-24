from django.db import models
from django.utils.text import slugify


# Create your models here.

class Guide(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField()
    published = models.DateField(auto_now_add=True)

    meta_description = models.CharField(
        max_length=160,
        blank=True
    )

    keywords = models.CharField(
        max_length=255,
        blank=True
    )

    image_url = models.URLField(blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
