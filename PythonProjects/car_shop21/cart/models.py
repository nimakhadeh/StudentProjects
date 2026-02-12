from django.db import models
from django.conf import settings


class Cart(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='کاربر'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')
    
    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبدهای خرید'
    
    def __str__(self):
        return f"سبد {self.user}"
    
    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())
    
    def get_total_items(self):
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='سبد'
    )
    car = models.ForeignKey(
        'cars.Car',
        on_delete=models.CASCADE,
        verbose_name='خودرو'
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name='تعداد')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ افزودن')
    
    class Meta:
        verbose_name = 'آیتم سبد'
        verbose_name_plural = 'آیتم‌های سبد'
        unique_together = ['cart', 'car']
    
    def __str__(self):
        return f"{self.car} × {self.quantity}"
    
    def get_total_price(self):
        return self.car.price * self.quantity
