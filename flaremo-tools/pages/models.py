from django.db import models
from tinymce.models import HTMLField

class Page(models.Model):
    is_published = models.BooleanField(default=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = HTMLField()

    def __str__(self):
        return self.title