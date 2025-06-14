from django.views.generic import ListView
from django.db.models import Avg
from django.core.cache import cache

from core.models import Nomenclature, Category
from core.constants import PAGINATOR_LIMIT


class Welcome(ListView):
    """Главная страница."""

    model = Nomenclature
    template_name = 'welcome/index.html'
    paginate_by = PAGINATOR_LIMIT

    def get_queryset(self):
        if not self.kwargs.get('cat_slug'):
            filter_pars = {'on_home': True}
        else:
            filter_pars = {'category__slug': self.kwargs['cat_slug']}
        return Nomenclature.objects.select_related(
            'category'
        ).filter(
            **filter_pars
        ).annotate(
            avg_rating=Avg('ratings__rating')
        ).order_by('-avg_rating')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = cache.get('categories')
        if categories is None:
            categories = list(Category.objects.all())
            cache.set('categories', categories, 2000)
        context['categories'] = categories
        return context
