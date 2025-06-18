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
        filter_pars = {}
        ordering = []

        find = self.request.GET.get('find_nom')
        if self.request.GET.get('category'):
            filter_pars['category__slug'] = self.request.GET['category']
        if find:
            filter_pars['name__iregex'] = f'.*{find}.*'
        if (sort_price := self.request.GET.get('sort_by_price')):
            ordering.append(('price' if sort_price == 'asc' else '-price'))

        if not filter_pars:
            filter_pars['on_home'] = True

        queryset = Nomenclature.objects.select_related(
            'category'
        ).filter(
            **filter_pars
        ).annotate(
            avg_rating=Avg('ratings__rating')
        ).order_by(*ordering or ('-avg_rating', 'name'))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = cache.get('categories')
        if not categories:
            # list побуждает ленивый кверисет отдать данные для кеша
            categories = list(Category.objects.all())
            cache.set('categories', categories, 2000)
        context['categories'] = categories
        return context
