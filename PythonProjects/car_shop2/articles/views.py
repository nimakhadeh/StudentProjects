from django.views.generic import ListView, DetailView
from .models import Article, Category


class ArticleListView(ListView):
    model = Article
    template_name = 'articles/list.html'
    context_object_name = 'articles'
    paginate_by = 12
    
    def get_queryset(self):
        return Article.objects.filter(status='published').order_by('-published_at')


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'articles/detail.html'
    context_object_name = 'article'
    slug_url_kwarg = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # افزایش بازدید
        self.object.views += 1
        self.object.save(update_fields=['views'])
        return context