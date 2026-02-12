from django.contrib import admin
from .models import Campaign, NotificationLog, UserDevice


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ['name', 'campaign_type', 'status', 'send_push', 'send_sms', 'created_at']
    list_filter = ['campaign_type', 'status', 'created_at']
    search_fields = ['name', 'title', 'message']
    date_hierarchy = 'created_at'


@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'channel', 'title', 'status', 'sent_at', 'clicked']
    list_filter = ['channel', 'status', 'clicked']
    search_fields = ['user__phone', 'title', 'message']
    readonly_fields = ['sent_at', 'delivered_at', 'clicked_at']


@admin.register(UserDevice)
class UserDeviceAdmin(admin.ModelAdmin):
    list_display = ['user', 'device_type', 'is_active', 'last_used']
    list_filter = ['device_type', 'is_active']