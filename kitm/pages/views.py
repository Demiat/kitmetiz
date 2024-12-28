from django.views.generic import TemplateView
from django.shortcuts import render

import core.constants as const


class About(TemplateView):
    """Статичная страница о Компании"""

    template_name = 'pages/about.html'


class Contact(TemplateView):
    """Статичная страница - Информация"""

    template_name = 'pages/contact.html'


def page_not_found(request, exception):
    return render(request, 'pages/404.html', status=const.NOT_FOUND)


def server_error(request):
    return render(request, 'pages/500.html',
                  status=const.INTERNAL_SERVER_ERROR)


def csrf_failure(request, reason=''):
    return render(request, 'pages/403csrf.html', status=const.FORBIDDEN)
