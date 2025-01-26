from django.views.generic import ListView

from .core.models import Nomenclature


class Welcome(ListView):
    """Главная страница."""

    model = Nomenclature
    template_name = 'welcome/index.html'
    queryset = Nomenclature.objects.filter(on_home=True)
