from django_filters.views import FilterView
from django.core.cache import cache

from core.models import Nomenclature, Category
from core.constants import PAGINATOR_LIMIT
from .filters import NomenclatureFilter


class Welcome(FilterView):
    """Главная страница."""

    model = Nomenclature
    template_name = 'welcome/index.html'
    paginate_by = PAGINATOR_LIMIT
    filterset_class = NomenclatureFilter

    # TODO убрать этот код после "переезда" на фильтр
    # def get_queryset(self):
    #     filter_pars = {}
    #     ordering = []

    #     find = self.request.GET.get('find_nom')
    #     if self.request.GET.get('category'):
    #         filter_pars['category__slug'] = self.request.GET['category']
    #     if find:
    #         filter_pars['name__iregex'] = f'.*{find}.*'
    #     if (sort_price := self.request.GET.get('sort_by_price')):
    #         ordering.append(('price' if sort_price == 'asc' else '-price'))

    #     if not filter_pars:
    #         filter_pars['on_home'] = True

    #     queryset = Nomenclature.objects.select_related(
    #         'category'
    #     ).filter(
    #         **filter_pars
    #     ).annotate(
    #         avg_rating=Avg('ratings__rating')
    #     ).order_by(*ordering or ('-avg_rating', 'name'))

    #     return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = cache.get('categories')
        if not categories:
            # list побуждает ленивый кверисет отдать данные для кеша
            categories = list(Category.objects.all())
            cache.set('categories', categories, 2000)

        context['categories'] = categories
        context['filter'] = self.filterset

        if self.request.GET.get('clear_category'):
            current_get_params = self.request.GET.copy()
            current_get_params.pop('category', None)
            current_get_params.pop('clear_category', None)
            self.request.GET = current_get_params

        if self.request.GET.get('category'):
            context['last_category'] = f'category={self.request.GET["category"]}'

        return context
