from django.views.generic.base import TemplateView


class MainPageView(TemplateView):
    """Главная страница"""
    template_name = 'index.html'
