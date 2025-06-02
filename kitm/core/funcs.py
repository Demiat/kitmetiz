import json
import base64
import os

from django.conf import settings
from dotenv import load_dotenv
import requests

from core.models import Nomenclature


load_dotenv()
NOM_FIXTURE = 'nom_from_1c.json'
NOM_IMAGES_FIXTURE = 'nom_images.json'
FINAL_TEXT = 'Создано {}, обновлено {} записей!'
BAD_CONNECTION = (
    'Нет соединения с эндпоинтом: {url}.'
    'Ошибка исключения: {exc_error}.'
)
NO_STATUS_OK = 'Ошибка {}: {}'
API_1C_URL = 'http://localhost/kit/hs/Products/get_prod?sklad=Основной склад'


class NoHttpStatusOk(Exception):
    """Плохой статус ответа HTTP."""

    pass


def update_or_create_from_1c(parsed_data):
    """Загружает и/или обновляет данные номенклатуры."""

    uids = set(Nomenclature.objects.values_list('UID', flat=True))

    for uid in parsed_data:
        product = dict(
            name=uid[0],
            quantity=uid[1],
            price=uid[2],
            article=uid[3],
            unit_of_measure=uid[4],
            category=uid[5],
        )
        to_create = []
        to_update = []
        if uid not in uids:
            to_create.append(Nomenclature(UID=uid, **product))
        else:
            to_update.append(Nomenclature(UID=uid, **product))

    if to_create:
        create_items = Nomenclature.objects.bulk_create(to_create)
    if to_update:
        update_items = Nomenclature.objects.bulk_update(
            to_update, list(product.keys())
        )
    return FINAL_TEXT.format(len(create_items), len(update_items))


def process_exchange_1C():
    """Обмен данными с 1С REST."""

    # Запрос к API 1C
    try:
        response = requests.get(
            API_1C_URL,
            auth=(
                os.getenv('1C_USERNAME', '').encode('utf-8'),
                os.getenv('1C_PASSWORD', '').encode('utf-8')
            )
        )
    except requests.RequestException as e:
        raise ConnectionError(
            BAD_CONNECTION.format(url=API_1C_URL, exc_error=e)
        )
    if response.status_code != 200:
        raise NoHttpStatusOk(
            NO_STATUS_OK.format(response.status_code, response.text))

    parsed_data = response.json()
    update_or_create_from_1c(parsed_data)


def process_exchange_1C_from_file():
    """Обмен данными с 1С из фикстуры."""

    fixture_path = os.path.join(settings.CORE_FIXTURES, NOM_FIXTURE)
    with open(f'{fixture_path}', 'r', encoding='utf-8') as file:
        parsed_data = json.load(file)

    update_or_create_from_1c(parsed_data)


def load_nomenclature_images():
    """Загружает изображения для существующей номенклатуры."""

    fixture_path = os.path.join(settings.CORE_FIXTURES, NOM_IMAGES_FIXTURE)
    with open(f'{fixture_path}', 'r', encoding='utf-8') as file:
        parsed_data = json.load(file)

    to_update = []
    for uid in parsed_data:
        if uid[6] != 'Нет Изображения':
            form, imgstr = uid[6].decode().split(';base64,')
            ext = form.split('/')[-1]
            decoded_image = base64.b64decode(imgstr)
            filename = f'{uid}.{ext}'
            # Сохраняем полученное изображение
            img_path = os.path.join(settings.MEDIA_NOM, filename)
            with open(img_path, 'wb') as output_file:
                output_file.write(decoded_image)
                # Заменим поле с изображением на путь к нему
                uid[6] = img_path
        else:
            uid[6] = None
        to_update.append(Nomenclature(UID=uid, image=uid[6]))

    update_items = Nomenclature.objects.bulk_update(
            to_update, ['image']
        )
    return f'Update {update_items} images'


# process_exchange_1C()
