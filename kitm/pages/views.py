from django.views.generic import TemplateView
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.http import HttpResponseRedirect
from django.urls import reverse

from core.constants import INTERNAL_SERVER_ERROR, NOT_FOUND, FORBIDDEN
from core.models import Nomenclature, Rating


class About(TemplateView):
    """Статичная страница о Компании"""

    template_name = 'pages/about.html'


class Contact(TemplateView):
    """Статичная страница - Информация"""

    template_name = 'pages/contact.html'


class NomenclatureCardDetail(LoginRequiredMixin, DetailView):
    """Детальная карточка номенклатуры."""

    model = Nomenclature
    template_name = 'pages/nom_card_detail.html'

    def post(self, request, *args, **kwargs):
        """Устанавливает рейтинг номенклатуры."""
        if request.POST.get('rating'):
            nomenclature = self.get_object()
            Rating.objects.update_or_create(
                nomenclature=nomenclature,
                author=request.user,
                defaults={'rating': int(request.POST['rating'])}
            )
        return HttpResponseRedirect(
            reverse(
                'pages:nom_card_detail',
                kwargs={'pk': self.kwargs.get('pk')}
            )
        )


def page_not_found(request, exception):
    return render(request, 'pages/404.html', status=NOT_FOUND)


def server_error(request):
    return render(request, 'pages/500.html',
                  status=INTERNAL_SERVER_ERROR)


def csrf_failure(request, reason=''):
    return render(request, 'pages/403csrf.html', status=FORBIDDEN)
