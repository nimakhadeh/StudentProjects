from django.db import models
from django.urls import reverse


class Car(models.Model):
    FUEL_CHOICES = [
        ('petrol', 'بنزین'),
        ('diesel', 'گازوئیل'),
        ('hybrid', 'هیبرید'),
        ('electric', 'برقی'),
    ]
    
    TRANSMISSION_CHOICES = [
        ('manual', 'دستی'),
        ('automatic', 'اتوماتیک'),
    ]
    
    # Basic info
    brand = models.CharField(max_length=100, verbose_name='برند')
    model = models.CharField(max_length=100, verbose_name='مدل')
    year = models.PositiveIntegerField(verbose_name='سال ساخت')
    price = models.DecimalField(max_digits=15, decimal_places=0, verbose_name='قیمت (تومان)')
    color = models.CharField(max_length=50, verbose_name='رنگ')
    stock = models.PositiveIntegerField(default=0, verbose_name='موجودی')
    image = models.ImageField(upload_to='cars/', verbose_name='تصویر', blank=True, null=True)
    description = models.TextField(verbose_name='توضیحات', blank=True)
    
    # Technical specs
    engine_capacity = models.CharField(max_length=20, verbose_name='حجم موتور', blank=True)
    fuel_type = models.CharField(max_length=20, choices=FUEL_CHOICES, default='petrol', verbose_name='نوع سوخت')
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES, default='manual', verbose_name='گیربکس')
    mileage = models.PositiveIntegerField(default=0, verbose_name='کارکرد (کیلومتر)')
    
    # Status
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')
    
    class Meta:
        verbose_name = 'خودرو'
        verbose_name_plural = 'خودروها'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.brand} {self.model} {self.year}"
    
    def get_absolute_url(self):
        return reverse('cars:detail', kwargs={'pk': self.pk})
    
    def is_available(self):
        return self.stock > 0 and self.is_active
    
    def formatted_price(self):
        return f"{self.price:,.0f}"
    
    def get_main_image(self):
        if self.image:
            return self.image.url
        return '/static/images/no-car.png'
