from django.db import models
from django.conf import settings
from django.urls import reverse


class DealerProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='dealer_profile',
        verbose_name="کاربر"
    )
    
    display_name = models.CharField(max_length=100, verbose_name="نام نمایشی")
    slug = models.SlugField(unique=True, verbose_name="اسلاگ")
    avatar = models.ImageField(upload_to='dealers/avatars/', null=True, blank=True, verbose_name="عکس")
    bio = models.TextField(blank=True, verbose_name="درباره")
    
    whatsapp_number = models.CharField(max_length=11, blank=True, verbose_name="واتساپ")
    show_phone = models.BooleanField(default=True, verbose_name="نمایش شماره")
    
    address = models.TextField(verbose_name="آدرس")
    lat = models.FloatField(null=True, blank=True, verbose_name="عرض جغرافیایی")
    lng = models.FloatField(null=True, blank=True, verbose_name="طول جغرافیایی")
    
    total_sales = models.PositiveIntegerField(default=0, verbose_name="تعداد فروش")
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0, verbose_name="امتیاز")
    
    is_verified = models.BooleanField(default=False, verbose_name="تایید شده")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")
    
    class Meta:
        verbose_name = "فروشنده"
        verbose_name_plural = "فروشندگان"
        ordering = ['-rating', '-total_sales']
    
    def __str__(self):
        return self.display_name
    
    def get_absolute_url(self):
        return reverse('dealers:detail', kwargs={'slug': self.slug})


class DealerReview(models.Model):
    dealer = models.ForeignKey(DealerProfile, on_delete=models.CASCADE, related_name='reviews', verbose_name="فروشنده")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="کاربر")
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)], verbose_name="امتیاز")
    comment = models.TextField(verbose_name="نظر")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ")
    
    class Meta:
        verbose_name = "نظر"
        verbose_name_plural = "نظرات"
        unique_together = ['dealer', 'user']