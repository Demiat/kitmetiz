from django.views.generic import ListView

from core.models import Nomenclature
from core.constants import PAGINATOR_LIMIT


class Welcome(ListView):
    """Главная страница."""

    model = Nomenclature
    template_name = 'welcome/index.html'
    queryset = Nomenclature.objects.filter(on_home=True)
    paginate_by = PAGINATOR_LIMIT
