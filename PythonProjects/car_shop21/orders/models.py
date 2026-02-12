from django.db import models
from django.conf import settings


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'در انتظار پرداخت'),
        ('processing', 'در حال پردازش'),
        ('shipped', 'ارسال شده'),
        ('delivered', 'تحویل داده شده'),
        ('cancelled', 'لغو شده'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='کاربر'
    )
    total_price = models.DecimalField(max_digits=15, decimal_places=0, verbose_name='مبلغ کل')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='وضعیت'
    )
    
    # Delivery info
    full_name = models.CharField(max_length=200, verbose_name='نام کامل')
    phone = models.CharField(max_length=11, verbose_name='تلفن')
    address = models.TextField(verbose_name='آدرس تحویل')
    postal_code = models.CharField(max_length=10, blank=True, verbose_name='کد پستی')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')
    
    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارشات'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"سفارش #{self.id} - {self.user}"
    
    def get_status_class(self):
        classes = {
            'pending': 'warning',
            'processing': 'info',
            'shipped': 'primary',
            'delivered': 'success',
            'cancelled': 'danger',
        }
        return classes.get(self.status, 'secondary')
    
    def get_status_display(self):
        for code, name in self.STATUS_CHOICES:
            if code == self.status:
                return name
        return self.status


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='سفارش'
    )
    car = models.ForeignKey(
        'cars.Car',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='خودرو'
    )
    quantity = models.PositiveIntegerField(verbose_name='تعداد')
    price = models.DecimalField(max_digits=15, decimal_places=0, verbose_name='قیمت واحد')
    
    class Meta:
        verbose_name = 'آیتم سفارش'
        verbose_name_plural = 'آیتم‌های سفارش'
    
    def __str__(self):
        return f"{self.car} × {self.quantity}"
    
    def get_total_price(self):
        return self.price * self.quantity
