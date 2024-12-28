# from django.shortcuts import render
from django.views.generic import TemplateView


class Welcome(TemplateView):
    """Главная страница."""

    template_name = 'welcome/index.html'
