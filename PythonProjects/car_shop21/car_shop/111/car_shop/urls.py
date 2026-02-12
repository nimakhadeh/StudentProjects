from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
from cars.models import Car


def home_view(request):
    """Home page view"""
    featured_cars = Car.objects.filter(is_active=True, stock__gt=0)[:8]
    latest_cars = Car.objects.filter(is_active=True, stock__gt=0).order_by('-created_at')[:4]
    
    context = {
        'featured_cars': featured_cars,
        'latest_cars': latest_cars,
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
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
