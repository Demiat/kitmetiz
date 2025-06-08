from django.views.generic import ListView

from core.models import Nomenclature

PAGINATOR_LIMIT = 6


class Welcome(ListView):
    """Главная страница."""

    model = Nomenclature
    template_name = 'welcome/index.html'
    queryset = Nomenclature.objects.filter(on_home=True)
    paginate_by = PAGINATOR_LIMIT
