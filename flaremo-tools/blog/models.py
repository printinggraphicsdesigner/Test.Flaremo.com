from django.db import models
from tinymce.models import HTMLField


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    # 👉 Featured Image
    featured_image = models.ImageField(
        upload_to='blogs/',
        blank=True,
        null=True
    )

    # 👉 Main Content (Rich Text)
    content = HTMLField()

    # 👉 Publish Control
    is_published = models.BooleanField(default=True)

    # 👉 Created Time
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']