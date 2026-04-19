from django.db import models
from django_summernote.fields import SummernoteTextField   # ← এই লাইনটা যোগ করো

# ==================== তোমার আগের Tool মডেল ====================
class Tool(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    url = models.CharField(max_length=300)
    icon = models.CharField(max_length=10, blank=True)
    is_active = models.BooleanField(default=True)

    def _str_(self):
        return self.name

    class Meta:
        ordering = ['name']


# ==================== নতুন BlogPost মডেল (Summernote সহ) ====================
class BlogPost(models.Model):
    title = models.CharField(max_length=200, verbose_name="ব্লগের শিরোনাম")
    slug = models.SlugField(unique=True, verbose_name="URL Slug")
    
    # এটাই Summernote Rich Editor
    content = SummernoteTextField(verbose_name="ব্লগের কনটেন্ট")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True, verbose_name="প্রকাশ করা হবে?")

    def _str_(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"