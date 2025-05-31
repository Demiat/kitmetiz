import json
import base64
import os

# from django.conf import settings
from dotenv import load_dotenv
import requests

import models


load_dotenv()
JSON_FIXTURE = '123.json'
FINAL_TEXT = 'Создано {}, обновлено {} записей!'
BAD_CONNECTION = (
    'Нет соединения с эндпоинтом: {url}.'
    'Ошибка исключения: {exc_error}.'
)
NO_STATUS_OK = 'Ошибка {}: {}'


class NoHttpStatusOk(Exception):
    """Плохой статус ответа HTTP."""

    pass


def process_exchange_1C():
    """Обмен данными с 1С."""
    # fixture_path = os.path.join(settings.CORE_FIXTURES, JSON_FIXTURE)
    # with open(f'{fixture_path}', 'r', encoding='utf-8') as file:
    #     parsed_data = json.load(file)

    # Запрос к API 1C
    url = 'http://localhost/kit/hs/Products/get_prod?sklad=Основной склад'
    try:
        response = requests.get(
            url,
            auth=(
                os.getenv('1C_USERNAME').encode('utf-8'),
                os.getenv('1C_PASSWORD').encode('utf-8')
            )
        )
    except requests.RequestException as e:
        raise ConnectionError(
            BAD_CONNECTION.format(url=url, exc_error=e)
        )
    if response.status_code != 200:
        raise NoHttpStatusOk(
            NO_STATUS_OK.format(response.status_code, response.text))
    parsed_data = response.json()

    # Обходим структуру
    for uid in parsed_data:
        product = dict(
            name=uid[0],
            quantity=uid[1],
            price=uid[2],
            article=uid[3],
            unit_of_measure=uid[4],
            category=uid[5],
            # image=uid[6],
        )
        # if product['image'] != 'Нет Изображения':
        #     # image_base64_bytes = product['image'].encode('ascii')
        #     # decoded_image = base64.b64decode(image_base64_bytes)
        #     form, imgstr = product['image'].decode().split(';base64,')
        #     ext = form.split('/')[-1]
        #     decoded_image = base64.b64decode(imgstr)
        #     filename = f'{uid}.{ext}'
        #     # Сохраняем полученное изображение
        #     img_path = os.path.join(settings.MEDIA_NOM, filename)
        #     with open(img_path, 'wb') as output_file:
        #         output_file.write(decoded_image)
        #         # Заменим поле с изображением на путь к нему
        #         product['image'] = img_path
        # else:
        #     product['image'] = None

        to_create = []
        to_update = []
        uids = set(models.Nomenclature.objects.values_list('UID', flat=True))
        if uid not in uids:
            to_create.append(models.Nomenclature(UID=uid, **product))
        else:
            to_update.append(models.Nomenclature(UID=uid, **product))

        if to_create:
            create_items = models.Nomenclature.objects.bulk_create(to_create)
        if to_update:
            update_items = models.Nomenclature.objects.bulk_update(
                to_update, list(product.keys())
            )
    return FINAL_TEXT.format(len(create_items), len(update_items))


process_exchange_1C()
