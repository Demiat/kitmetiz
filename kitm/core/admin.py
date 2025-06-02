import pickle

from django.contrib import admin
from django.template.response import TemplateResponse
from django_apscheduler.models import DjangoJob, DjangoJobExecution
from django.utils.encoding import force_str

from .funcs import process_exchange_1C_from_file, load_nomenclature_images

DESERIALIZED_ERROR = 'Ошибка десериализации данных: {e}'


class CustomAdminSite(admin.AdminSite):
    site_header = 'KIT-Metiz Admin Site'
    site_title = 'My Custom Admin'
    empty_value_display = '-пусто-'

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        my_urls = [
            path(
                'from-1c/',
                self.admin_view(self.exchange_1С),
                name='from_1c'
            ),
            path(
                'load-images/',
                self.admin_view(self.load_images),
                name='load_images'
            ),
        ]
        return my_urls + urls

    def _exchange_process(self, request, func):
        message = None
        if request.method == 'POST':
            message = func()
        # Наследуем контекст от родительского класса AdminSite
        context = self.each_context(request)
        context.update({
            'title': 'Администрирование сайта',
            # Получим список приложений(моделей) для шаблона index
            'app_list': self.get_app_list(request),
            'message': message,  # Добавим свои данные
        })
        return TemplateResponse(request, 'admin/index.html', context)

    def exchange_1С(self, request):
        self._exchange_process(request, process_exchange_1C_from_file)

    def load_images(self, request):
        self._exchange_process(request, load_nomenclature_images)


class ProxyDjangoJob(DjangoJob):
    """Прокси-класс для переопределения метаданных моделей
    библиотеки django-appsheduler."""

    class Meta:
        proxy = True
        verbose_name = "Задания Django"
        verbose_name_plural = "Задания Django"


class ProxyDjangoJobExecution(DjangoJobExecution):
    """Прокси-класс для переопределения метаданных моделей
    библиотеки django-appsheduler."""

    class Meta:
        proxy = True
        verbose_name = "Выполненное задание Django"
        verbose_name_plural = "Выполненные задания Django"


class DjangoJobAdmin(admin.ModelAdmin):
    list_display = ('id', 'next_run_time', 'readable_job_state')
    list_filter = ('next_run_time',)
    search_fields = ('readable_job_state',)

    @admin.display(description='Триггер')
    def readable_job_state(self, obj):
        try:
            return force_str(pickle.loads(obj.job_state)['trigger'])
        except Exception as e:
            return DESERIALIZED_ERROR.format(e=force_str(e))


class DjangoJobExecutionAdmin(admin.ModelAdmin):
    list_display = ('id', 'run_time', 'job', 'exception', 'status')
    list_filter = ('run_time', 'status')
    search_fields = ('run_time',)


сustom_admin_site = CustomAdminSite(name='myadmin')
сustom_admin_site.register(ProxyDjangoJob, DjangoJobAdmin)
сustom_admin_site.register(ProxyDjangoJobExecution, DjangoJobExecutionAdmin)
