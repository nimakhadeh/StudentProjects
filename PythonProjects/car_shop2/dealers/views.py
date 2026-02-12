from django.views.generic import ListView, DetailView
from django.db.models import Q, Avg, Count
from .models import DealerProfile


class DealerListView(ListView):
    model = DealerProfile
    template_name = 'dealers/list.html'
    context_object_name = 'dealers'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = super().get_queryset().filter(is_active=True, is_verified=True)
        
        # جستجو
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(display_name__icontains=q) | Q(address__icontains=q)
            )
        
        return queryset.annotate(
            reviews_count=Count('reviews'),
            avg_rating=Avg('reviews__rating')
        )


class DealerDetailView(DetailView):
    model = DealerProfile
    template_name = 'dealers/detail.html'
    context_object_name = 'dealer'
    slug_url_kwarg = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # خودروهای فروشنده
        context['cars'] = self.object.user.car_set.filter(is_active=True, is_sold=False)[:12]
        # نظرات
        context['reviews'] = self.object.reviews.select_related('user')[:10]
        return context