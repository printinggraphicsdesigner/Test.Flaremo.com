from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Tool, BlogPost

@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active')
    prepopulated_fields = {"slug": ("name",)}

# BlogPost Admin with Summernote
@admin.register(BlogPost)
class BlogPostAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)        # ← Summernote এনাবল
    list_display = ['title', 'is_published', 'created_at']
    list_filter = ['is_published']
    search_fields = ['title']