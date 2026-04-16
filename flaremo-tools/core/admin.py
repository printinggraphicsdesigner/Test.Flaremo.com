from django.contrib import admin
from .models import Tool

@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active')
    prepopulated_fields = {"slug": ("name",)}
