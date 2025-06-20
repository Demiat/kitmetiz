import django_filters
from core.models import Nomenclature
from django.db.models import Avg
from django import forms
from django.forms.widgets import Select


class CustomSelectWidget(Select):
    """Переопределим стиль селекта."""

    def __init__(self, attrs=None, *args, **kwargs):
        super().__init__(attrs={'class': 'form-select form-select-sm me-2'})


class NomenclatureFilter(django_filters.FilterSet):
    """Фильтрует и сортирует номенклатуру."""

    category = django_filters.CharFilter(
        field_name='category__slug',
        label=False,
        widget=forms.HiddenInput(),
    )

    find_nom = django_filters.CharFilter(
        field_name='name',
        lookup_expr='iregex',
        label=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control flex-grow-1 w-100 me-2',
            'type': 'search',
            'placeholder': 'Поиск по номенклатуре',
            'aria-label': 'Search'
        })
    )

    # Фильтр сортировки по цене
    sort_by_price = django_filters.OrderingFilter(
        fields=(('price', 'price'),),
        widget=CustomSelectWidget,
        label=False,
        choices=[
            ('price', 'Возрастание цены'),
            ('-price', 'Убывание цены')
        ],
    )

    # Фильтр сортировки по рейтингу
    sort_by_rating = django_filters.OrderingFilter(
        fields=(('ratings__rating', 'rating'),),
        widget=CustomSelectWidget,
        label=False,
        choices=[
            ('-ratings__rating', 'От высшего к низшему'),
            ('ratings__rating', 'От низкого к высокому')
        ],
    )

    # Фильтр сортировки по названию
    sort_by_name = django_filters.OrderingFilter(
        fields=(('name', 'name'),),
        widget=CustomSelectWidget,
        label=False,
        choices=[
            ('name', 'От А до Я'),
            ('-name', 'От Я до А')
        ],
    )

    class Meta:
        model = Nomenclature
        fields = [
            'find_nom', 'sort_by_price', 'sort_by_rating', 'sort_by_name'
        ]

    @property
    def qs(self):
        result = super().qs.annotate(
            avg_rating=Avg('ratings__rating')
        ).select_related(
            'category'
        )
        orderings = []
        if self.data.get('sort_by_price'):
            orderings.append(self.data['sort_by_price'])
        if self.data.get('sort_by_rating'):
            orderings.append(
                'avg_rating'
                if self.data['sort_by_rating'] != '-ratings__rating'
                else '-avg_rating'
            )
        else:
            orderings.append('-avg_rating')
        if self.data.get('sort_by_name'):
            orderings.append(self.data['sort_by_name'])
        return result.order_by(*orderings)
