from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('customer', 'مشتری'),
        ('admin', 'مدیر'),
    ]
    
    phone = models.CharField(max_length=11, verbose_name='تلفن همراه', blank=True)
    address = models.TextField(verbose_name='آدرس', blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer', verbose_name='نقش')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت‌نام')
    
    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'
    
    def is_admin_user(self):
        return self.role == 'admin' or self.is_staff or self.is_superuser
    
    def get_full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    
    def __str__(self):
        return self.get_full_name()
