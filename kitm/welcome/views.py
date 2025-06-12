from django.views.generic import ListView
from django.db.models import Avg

from core.models import Nomenclature
from core.constants import PAGINATOR_LIMIT


class Welcome(ListView):
    """Главная страница."""

    model = Nomenclature
    template_name = 'welcome/index.html'
    queryset = Nomenclature.objects.filter(
        on_home=True
        ).annotate(avg_rating=Avg('ratings__rating')).order_by('-avg_rating')
    paginate_by = PAGINATOR_LIMIT
