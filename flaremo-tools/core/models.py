from django.db import models

class Tool(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    url = models.CharField(max_length=300)  # route path (e.g. /tools/word-to-pdf/)
    icon = models.ImageField(upload_to='icons/', blank=True, null=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
