from django.contrib import admin
from .models import Tool


# ==================== Tool Admin ====================
@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon', 'is_active', 'url')
    list_filter = ('is_active',)
    search_fields = ('name', 'description', 'url')
    prepopulated_fields = {"slug": ("name",)}

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description')
        }),
        ('Tool Settings', {
            'fields': ('url', 'icon', 'is_active')
        }),
    )