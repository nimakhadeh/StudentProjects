from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = [
        'username', 
        'email', 
        'first_name', 
        'last_name', 
        'phone',
        'user_type',  # ← 'role' به 'user_type' تغییر کرد
        'is_staff',
        'date_joined'
    ]
    
    list_filter = [
        'user_type',  # ← 'role' به 'user_type' تغییر کرد
        'is_staff', 
        'is_superuser', 
        'is_active',
        'allow_marketing_sms',
        'allow_marketing_push'
    ]
    
    fieldsets = UserAdmin.fieldsets + (
        ('اطلاعات اضافی', {
            'fields': (
                'phone',
                'address',  # ← اضافه شد
                'birth_date',
                'user_type',
                'allow_marketing_sms',
                'allow_marketing_push',
                'allow_location_tracking',
            )
        }),
        ('موقعیت مکانی', {
            'fields': (
                'last_lat',
                'last_lng',
                'location_updated_at',
            ),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('اطلاعات اضافی', {
            'fields': ('phone', 'user_type')
        }),
    )
    
    search_fields = ['username', 'email', 'phone', 'first_name', 'last_name']
    
    readonly_fields = ['location_updated_at']