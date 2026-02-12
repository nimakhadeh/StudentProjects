from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['order', 'amount', 'gateway', 'status', 'tracking_code', 'created_at']
    list_filter = ['status', 'gateway', 'created_at']
    search_fields = ['tracking_code', 'order__id']
    readonly_fields = ['tracking_code', 'created_at']
