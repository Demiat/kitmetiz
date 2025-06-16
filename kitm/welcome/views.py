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
        find = self.request.GET.get('find_nom')
        if self.kwargs.get('cat_slug'):
            filter_pars = {'category__slug': self.kwargs['cat_slug']}
        elif find:
            filter_pars = {'name__iregex': f'.*{find}.*'}
        else:
            filter_pars = {'on_home': True}

        queryset = Nomenclature.objects.select_related(
            'category'
        ).filter(
            **filter_pars
        ).annotate(
            avg_rating=Avg('ratings__rating')
        ).order_by('-avg_rating', 'name')

        if find:
            return queryset
            # return queryset[:PAGINATOR_LIMIT]

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
