from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Car


class CarListView(ListView):
    model = Car
    template_name = 'cars/car_list.html'
    context_object_name = 'cars'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Car.objects.filter(is_active=True)
        
        # Search
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(brand__icontains=search) |
                Q(model__icontains=search) |
                Q(description__icontains=search)
            )
        
        # Brand filter
        brand = self.request.GET.get('brand')
        if brand:
            queryset = queryset.filter(brand__iexact=brand)
        
        # Price range
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        # Year filter
        year = self.request.GET.get('year')
        if year:
            queryset = queryset.filter(year=year)
        
        # Sorting
        sort = self.request.GET.get('sort')
        if sort == 'price_asc':
            queryset = queryset.order_by('price')
        elif sort == 'price_desc':
            queryset = queryset.order_by('-price')
        elif sort == 'year_desc':
            queryset = queryset.order_by('-year')
        elif sort == 'year_asc':
            queryset = queryset.order_by('year')
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get unique brands for filter
        context['brands'] = Car.objects.filter(is_active=True).exclude(
            brand__exact=''
        ).values_list('brand', flat=True).distinct().order_by('brand')
        
        # Get unique years for filter
        context['years'] = Car.objects.filter(is_active=True).values_list(
            'year', flat=True
        ).distinct().order_by('-year')
        
        # Preserve query params for pagination
        query_params = self.request.GET.copy()
        if 'page' in query_params:
            del query_params['page']
        context['query_params'] = query_params.urlencode()
        
        return context


class CarDetailView(DetailView):
    model = Car
    template_name = 'cars/car_detail.html'
    context_object_name = 'car'
    
    def get_queryset(self):
        return Car.objects.filter(is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Related cars (same brand, exclude current)
        context['related_cars'] = Car.objects.filter(
            brand=self.object.brand,
            is_active=True
        ).exclude(id=self.object.id)[:4]
        return context
