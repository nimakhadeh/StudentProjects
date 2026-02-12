from django.db import models
from django.conf import settings


class Lead(models.Model):
    STATUS_CHOICES = [
        ('new', 'جدید'),
        ('contacted', 'تماس گرفته شده'),
        ('interested', 'علاقه‌مند'),
        ('test_drive', 'تست درایو'),
        ('negotiating', 'در حال مذاکره'),
        ('closed_won', 'فروخته شد'),
        ('closed_lost', 'از دست رفت'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, verbose_name="نام")
    phone = models.CharField(max_length=11, verbose_name="موبایل")
    source = models.CharField(max_length=20, default='website', verbose_name="منبع")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="وضعیت")
    
    budget_min = models.PositiveBigIntegerField(null=True, blank=True, verbose_name="حداقل بودجه")
    budget_max = models.PositiveBigIntegerField(null=True, blank=True, verbose_name="حداکثر بودجه")
    
    notes = models.TextField(blank=True, verbose_name="یادداشت")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    
    class Meta:
        verbose_name = "سرنخ"
        verbose_name_plural = "سرنخ‌ها"