from django.contrib import admin
from .models import Item

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'category', 'daily_rate', 'available', 'usage_count']
    list_filter = ['category', 'available']
    search_fields = ['title', 'owner__username']
