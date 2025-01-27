from django.contrib.admin import AdminSite
from django.template.response import TemplateResponse
from django.http import HttpRequest, HttpResponseRedirect
from django.conf.settings import CORE_FIXTURES


class CustomAdminSite(AdminSite):
    site_header = 'KIT-Metiz Admin Site'
    site_title = 'My Custom Admin'
    # index_title = ''

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        my_urls = [
            path(
                'from_1c/',
                self.admin_view(self.exchange_1С),
                name='from_1c'
            ),
        ]
        return my_urls + urls

    def exchange_1С(self, request: HttpRequest):
        if request.method == 'POST':
            # import json
            print("Кнопка была нажата!")
            # with open(
            # f'{CORE_FIXTURES}/123.json', 'r', encoding='utf-8'
            # ) as file:
            #     parsed_data = json.load(file)

            # # Обходим структуру
            # for uid in parsed_data:
            #     product_info = parsed_data[uid]
            #     print(f"Уникальный идентификатор: {uid}")
            #     print(f"Наименование: {product_info[0]}")
            #     print(f"Количество: {product_info[1]}")
            #     print(f"Цена: {product_info[2]}")
            #     print(f"Артикул: {product_info[3]}")
            #     print(f"Единица измерения: {product_info[4]}")
            #     print(f"Категория: {product_info[5]}\n")
            return HttpResponseRedirect('/admin/')

        # context = dict(
        #     self.each_context(request),
        # )
        # return TemplateResponse(request, 'admin/from_1c.html', context)


сustom_admin_site = CustomAdminSite(name='myadmin')
