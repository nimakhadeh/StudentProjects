from django.contrib import admin
from .models import DealerProfile, DealerReview


@admin.register(DealerProfile)
class DealerProfileAdmin(admin.ModelAdmin):
    list_display = ['display_name', 'user', 'rating', 'total_sales', 'is_verified', 'is_active']
    list_filter = ['is_verified', 'is_active']
    search_fields = ['display_name', 'user__phone', 'address']
    prepopulated_fields = {'slug': ('display_name',)}


@admin.register(DealerReview)
class DealerReviewAdmin(admin.ModelAdmin):
    list_display = ['dealer', 'user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']