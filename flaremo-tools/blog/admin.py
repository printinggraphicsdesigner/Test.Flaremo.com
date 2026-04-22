from django.contrib import admin
from .models import BlogPost

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'tool', 'page', 'is_published', 'created_at']
    list_editable = ['is_published']
    list_filter = ['tool', 'page', 'is_published']
    search_fields = ['title']
    prepopulated_fields = {"slug": ("title",)}