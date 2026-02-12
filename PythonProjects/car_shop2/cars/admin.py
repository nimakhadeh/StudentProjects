from django.contrib import admin
from .models import Car


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['brand', 'model', 'year', 'price', 'stock', 'is_active', 'created_at']
    list_filter = ['brand', 'year', 'is_active', 'fuel_type', 'transmission']
    search_fields = ['brand', 'model', 'description']
    list_editable = ['price', 'stock', 'is_active']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('brand', 'model', 'year', 'price', 'color', 'stock', 'image', 'description')
        }),
        ('Technical Specs', {
            'fields': ('engine_capacity', 'fuel_type', 'transmission', 'mileage'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
