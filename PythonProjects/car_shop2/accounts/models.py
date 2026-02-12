from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone = models.CharField(max_length=11, unique=True, verbose_name="موبایل", null=True, blank=True)
    address = models.TextField(null=True, blank=True, verbose_name="آدرس")
    birth_date = models.DateField(null=True, blank=True, verbose_name="تاریخ تولد")
    
    allow_marketing_sms = models.BooleanField(default=True, verbose_name="اجازه پیامک")
    allow_marketing_push = models.BooleanField(default=True, verbose_name="اجازه پوش")
    allow_location_tracking = models.BooleanField(default=False, verbose_name="اجازه موقعیت")
    
    last_lat = models.FloatField(null=True, blank=True, verbose_name="عرض جغرافیایی")
    last_lng = models.FloatField(null=True, blank=True, verbose_name="طول جغرافیایی")
    location_updated_at = models.DateTimeField(null=True, blank=True, verbose_name="آخرین موقعیت")
    
    USER_TYPE_CHOICES = [
        ('customer', 'مشتری'),
        ('dealer', 'فروشنده'),
        ('admin', 'مدیر'),
    ]
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='customer', verbose_name="نوع")
    
    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"
    
    def is_dealer(self):
        return self.user_type == 'dealer'
    
    def __str__(self):
        return f"{self.phone or self.username} - {self.get_user_type_display()}"