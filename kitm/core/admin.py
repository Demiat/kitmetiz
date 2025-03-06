import json
import base64
import os

from django.contrib import admin
from django.template.response import TemplateResponse
from django.conf import settings
from django_apscheduler.models import DjangoJob, DjangoJobExecution

from . models import Nomenclature

JSON_FIXTURE = '123.json'


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
                name='from-1c'
            ),
        ]
        return my_urls + urls

    @staticmethod
    def process_exchange_1C():
        fixture_path = os.path.join(settings.CORE_FIXTURES, JSON_FIXTURE)
        with open(f'{fixture_path}', 'r', encoding='utf-8') as file:
            parsed_data = json.load(file)
        # Обходим структуру
        for uid in parsed_data:
            product = parsed_data[uid]
            if product[6] != 'Нет Изображения':
                image_base64_bytes = product[6].encode('ascii')
                decoded_image = base64.b64decode(image_base64_bytes)
                # Сохраняем полученное изображение
                img_path = os.path.join(
                    settings.MEDIA_NOM,
                    f'{uid}.jpg'
                )
                with open(img_path, 'wb') as output_file:
                    output_file.write(decoded_image)
            Nomenclature.objects.update_or_create(
                UID=uid,
                defaults=dict(
                    name=product[0],
                    quantity=product[1],
                    price=product[2],
                    article=product[3],
                    unit_of_measure=product[4],
                    category=product[5],
                    image=img_path,
                )
            )
            img_path = ''
        return f'Обработано {len(parsed_data)} записей!'

    def exchange_1С(self, request):
        message = None
        if request.method == 'POST':
            message = self.process_exchange_1C()
        # Наследуем контекст от родительского класса AdminSite
        context = self.each_context(request)
        context.update({
            'title': 'Администрирование сайта',
            # Получим список приложений(моделей) для шаблона index
            'app_list': self.get_app_list(request),
            'message': message,  # Добавим свои данные
        })
        return TemplateResponse(request, 'admin/index.html', context)


class DjangoJobAdmin(admin.ModelAdmin):
    pass
    # list_display = ('id', 'name', 'next_run_time', 'job_state')
   # list_filter = ('name', 'next_run_time')
   # search_fields = ['name']

# Класс для модели DjangoJobExecution


class DjangoJobExecutionAdmin(admin.ModelAdmin):
    pass
    # list_display = ('id', 'run_time', 'job', 'exception', 'status')
   # list_filter = ('run_time', 'job__name', 'status')
   # search_fields = ['job__name']


сustom_admin_site = CustomAdminSite(name='myadmin')
сustom_admin_site.register(DjangoJob, DjangoJobAdmin)
сustom_admin_site.register(DjangoJobExecution, DjangoJobExecutionAdmin)
