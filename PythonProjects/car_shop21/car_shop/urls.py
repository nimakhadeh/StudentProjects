from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
from cars.models import Car
from dealers.models import DealerProfile
from articles.models import Article


def home_view(request):
    """Home page view"""
    featured_cars = Car.objects.filter(is_active=True, stock__gt=0)[:8]
    latest_cars = Car.objects.filter(is_active=True, stock__gt=0).order_by('-created_at')[:4]
    
    # فروشندگان برتر (۴ تای اول)
    top_dealers = DealerProfile.objects.filter(is_active=True, is_verified=True)[:4]
    
    # ۳ مقاله آخر
    latest_articles = Article.objects.filter(status='published').order_by('-published_at')[:3]
    
    context = {
        'featured_cars': featured_cars,
        'latest_cars': latest_cars,
        'top_dealers': top_dealers,
        'latest_articles': latest_articles,
    }
    return render(request, 'home.html', context)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('accounts/', include('accounts.urls')),
    path('cars/', include('cars.urls', namespace='cars')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('payment/', include('payment.urls', namespace='payment')),
    path('dealers/', include('dealers.urls', namespace='dealers')),
    path('articles/', include('articles.urls', namespace='articles')),
    path('notifications/', include('notifications.urls', namespace='notifications')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)