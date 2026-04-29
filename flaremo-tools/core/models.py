from django.db import models
from tinymce.models import HTMLField   # 👈 IMPORT

class Tool(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    is_published = models.BooleanField(default=True)

    content = HTMLField(blank=True, null=True)   # ✅ CHANGE THIS

    url = models.CharField(max_length=300)
    icon = models.CharField(max_length=10, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
