from django.db import models
from django.conf import settings


class Campaign(models.Model):
    """کمپین‌های تبلیغاتی"""
    CAMPAIGN_TYPES = [
        ('location', 'بر اساس موقعیت'),
        ('birthday', 'تبریک تولد'),
        ('manual', 'دستی'),
        ('scheduled', 'زمان‌بندی شده'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'پیش‌نویس'),
        ('active', 'فعال'),
        ('paused', 'متوقف'),
        ('completed', 'تمام شده'),
    ]
    
    name = models.CharField(max_length=200, verbose_name="نام کمپین")
    campaign_type = models.CharField(max_length=20, choices=CAMPAIGN_TYPES, verbose_name="نوع")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name="وضعیت")
    
    # Content
    title = models.CharField(max_length=200, verbose_name="عنوان")
    message = models.TextField(verbose_name="متن پیام")
    link = models.URLField(blank=True, verbose_name="لینک")
    
    # For location-based
    target_lat = models.FloatField(null=True, blank=True, verbose_name="عرض جغرافیایی هدف")
    target_lng = models.FloatField(null=True, blank=True, verbose_name="طول جغرافیایی هدف")
    radius_km = models.PositiveIntegerField(default=5, verbose_name="شعاع (کیلومتر)")
    
    # For scheduled
    scheduled_at = models.DateTimeField(null=True, blank=True, verbose_name="زمان ارسال")
    
    # Channels
    send_push = models.BooleanField(default=True, verbose_name="ارسال پوش")
    send_sms = models.BooleanField(default=False, verbose_name="ارسال پیامک")
    send_whatsapp = models.BooleanField(default=False, verbose_name="ارسال واتساپ")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="ایجاد کننده")
    
    class Meta:
        verbose_name = "کمپین"
        verbose_name_plural = "کمپین‌ها"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.get_campaign_type_display()})"


class NotificationLog(models.Model):
    """لاگ ارسال‌ها"""
    STATUS_CHOICES = [
        ('pending', 'در صف'),
        ('sent', 'ارسال شد'),
        ('failed', 'ناموفق'),
        ('delivered', 'تحویل داده شد'),
    ]
    
    CHANNEL_CHOICES = [
        ('push', 'پوش نوتیفیکیشن'),
        ('sms', 'پیامک'),
        ('whatsapp', 'واتساپ'),
        ('email', 'ایمیل'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="کاربر")
    campaign = models.ForeignKey(Campaign, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="کمپین")
    
    channel = models.CharField(max_length=20, choices=CHANNEL_CHOICES, verbose_name="کانال")
    title = models.CharField(max_length=200, verbose_name="عنوان")
    message = models.TextField(verbose_name="متن")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="وضعیت")
    error_message = models.TextField(blank=True, verbose_name="خطا")
    
    sent_at = models.DateTimeField(null=True, blank=True, verbose_name="زمان ارسال")
    delivered_at = models.DateTimeField(null=True, blank=True, verbose_name="زمان تحویل")
    
    clicked = models.BooleanField(default=False, verbose_name="کلیک شده")
    clicked_at = models.DateTimeField(null=True, blank=True, verbose_name="زمان کلیک")
    
    class Meta:
        verbose_name = "لاگ اعلان"
        verbose_name_plural = "لاگ اعلان‌ها"
        ordering = ['-sent_at']


class UserDevice(models.Model):
    """دستگاه‌های کاربر برای FCM"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='devices', verbose_name="کاربر")
    device_token = models.CharField(max_length=500, verbose_name="توکن دستگاه")
    device_type = models.CharField(max_length=20, choices=[('android', 'اندروید'), ('ios', 'iOS'), ('web', 'وب')], verbose_name="نوع دستگاه")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")
    last_used = models.DateTimeField(auto_now=True, verbose_name="آخرین استفاده")
    
    class Meta:
        verbose_name = "دستگاه"
        verbose_name_plural = "دستگاه‌ها"
        unique_together = ['user', 'device_token']