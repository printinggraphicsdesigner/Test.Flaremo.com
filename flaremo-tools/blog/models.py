from django.db import models
from tinymce.models import HTMLField
from core.models import Tool

# 👉 Page choices (static pages)
PAGE_CHOICES = [
    ('about', 'About Page'),
    ('contact', 'Contact Page'),
    ('privacy', 'Privacy Policy'),
    ('terms', 'Terms & Services'),
    ('disclaimer', 'Disclaimer'),
]

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)


    featured_image = models.ImageField(upload_to='blog/', blank=True, null=True)  # 👈 ADD

    content = HTMLField()

    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    # 👉 Tool select
    tool = models.ForeignKey(
        Tool,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='blogs'
    )

    # 👉 Page select
    page = models.CharField(
        max_length=50,
        choices=PAGE_CHOICES,
        blank=True,
        null=True
    )

    # 👉 Content
    content = HTMLField()

    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title