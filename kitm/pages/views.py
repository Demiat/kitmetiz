from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView

from core.constants import INTERNAL_SERVER_ERROR, NOT_FOUND, FORBIDDEN
from core.models import Nomenclature, Rating


class About(TemplateView):
    """Статичная страница о Компании"""

    template_name = 'pages/about.html'


class Contact(TemplateView):
    """Статичная страница - Информация"""

    template_name = 'pages/contact.html'


class NomenclatureCardDetail(DetailView):
    """Детальная карточка номенклатуры."""

    model = Nomenclature
    template_name = 'pages/nom_card_detail.html'

    def get_context_data(self, **kwargs):
        """Добавляет рейтинг номенклатуры от автора в контекст шаблона."""
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            try:
                context['current_user_rating'] = Rating.objects.get(
                    nomenclature=self.object,
                    author=self.request.user
                ).rating
            except Rating.DoesNotExist:
                context['current_user_rating'] = None
        return context

    def post(self, request, *args, **kwargs):
        """Устанавливает рейтинг номенклатуры."""
        if (
            request.user.is_authenticated
            and (rating := request.POST.get('rating'))
        ):
            nomenclature = self.get_object()
            # Для предотвращения замены авторства сначала найдем
            # существующий рейтинг от текущего пользователя
            existing_rating = Rating.objects.filter(
                nomenclature=nomenclature,
                author=request.user
            ).first()

            # Обновляем, если автор и текущий пользователь совпали
            if existing_rating:
                existing_rating.rating = int(rating)
                existing_rating.save()
            # Либо создаем новый рейтинг от текущего пользователя
            else:
                Rating.objects.create(
                    nomenclature=nomenclature,
                    author=request.user,
                    rating=int(rating)
                )
        return redirect(
            'pages:nom_card_detail',
            pk=self.kwargs.get('pk')
        )


def page_not_found(request, exception):
    return render(request, 'pages/404.html', status=NOT_FOUND)


def server_error(request):
    return render(request, 'pages/500.html',
                  status=INTERNAL_SERVER_ERROR)


def csrf_failure(request, reason=''):
    return render(request, 'pages/403csrf.html', status=FORBIDDEN)
