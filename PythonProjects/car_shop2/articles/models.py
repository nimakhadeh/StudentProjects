from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام")
    slug = models.SlugField(unique=True, verbose_name="اسلاگ")
    
    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"
    
    def __str__(self):
        return self.name


class Article(models.Model):
    STATUS_CHOICES = [
        ('draft', 'پیش‌نویس'),
        ('published', 'منتشر شده'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="عنوان")
    slug = models.SlugField(unique=True, verbose_name="اسلاگ")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="دسته‌بندی")
    
    meta_title = models.CharField(max_length=70, blank=True, verbose_name="عنوان سئو")
    meta_description = models.CharField(max_length=160, blank=True, verbose_name="توضیحات متا")
    
    excerpt = models.TextField(verbose_name="خلاصه")
    content = models.TextField(verbose_name="محتوا")
    featured_image = models.ImageField(upload_to='articles/', verbose_name="تصویر")
    
    author = models.CharField(max_length=100, verbose_name="نویسنده")
    views = models.PositiveIntegerField(default=0, verbose_name="بازدید")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name="وضعیت")
    published_at = models.DateTimeField(null=True, blank=True, verbose_name="تاریخ انتشار")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "مقاله"
        verbose_name_plural = "مقالات"
        ordering = ['-published_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('articles:detail', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)