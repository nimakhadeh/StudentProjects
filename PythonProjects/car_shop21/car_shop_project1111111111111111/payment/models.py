from django.db import models


class Payment(models.Model):
    GATEWAY_CHOICES = [
        ('zarinpal', 'زرین‌پال'),
        ('mellat', 'بانک ملت'),
        ('saman', 'بانک سامان'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'در انتظار'),
        ('success', 'موفق'),
        ('failed', 'ناموفق'),
    ]
    
    order = models.ForeignKey(
        'orders.Order',
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='سفارش'
    )
    amount = models.DecimalField(max_digits=15, decimal_places=0, verbose_name='مبلغ')
    gateway = models.CharField(max_length=20, choices=GATEWAY_CHOICES, verbose_name='درگاه')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name='وضعیت')
    tracking_code = models.CharField(max_length=20, blank=True, null=True, verbose_name='کد رهگیری')
    error_message = models.TextField(blank=True, verbose_name='پیام خطا')
    paid_at = models.DateTimeField(blank=True, null=True, verbose_name='تاریخ پرداخت')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    
    class Meta:
        verbose_name = 'پرداخت'
        verbose_name_plural = 'پرداخت‌ها'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"پرداخت #{self.id} - {self.get_status_display()}"
