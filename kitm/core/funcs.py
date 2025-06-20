import json
import base64
import os

from django.conf import settings
from django.db import transaction
from dotenv import load_dotenv
import requests

from core.models import Nomenclature, Category


load_dotenv()
NOM_FIXTURE = 'nom_from_1c.json'
FINAL_TEXT = 'Записей создано: {}, обновлено: {}'
BAD_CONNECTION = (
    'Нет соединения с эндпоинтом: {url}.'
    'Ошибка исключения: {exc_error}.'
)
NO_STATUS_OK = 'Ошибка {}: {}'
API_1C_URL = 'http://localhost/kit/hs/Products/get_prod?sklad=Основной склад'


class NoHttpStatusOk(Exception):
    """Плохой статус ответа HTTP."""

    pass


@transaction.atomic
def update_or_create_from_1c(parsed_data):
    """Загружает и/или обновляет данные номенклатуры."""
    # Предварительно получим плоский список uid номенклатуры
    uids = set(Nomenclature.objects.values_list('UID', flat=True))

    # Предварительно выбираем все категории из базы
    categories_by_slug = {obj.slug: obj for obj in Category.objects.all()}

    to_create = []
    to_update = []
    for uid, value in parsed_data.items():

        category_slug = value[5][1]  # Получаем slug категории из фикстуры
        category_obj = categories_by_slug.get(category_slug)
        # Если категории нет в базе, то создадим ее и добавим в кэш.
        if not category_obj:
            category_obj = Category(name=value[5][0], slug=category_slug)
            category_obj.save()
            # Кэшируем новую категорию
            categories_by_slug[category_slug] = category_obj

        product = dict(
            name=value[0],
            quantity=value[1],
            price=value[2],
            article=value[3],
            unit_of_measure=value[4],
            category=category_obj,
            on_home=True  # Временно
        )
        if uid not in uids:
            to_create.append(Nomenclature(UID=uid, **product))
        else:
            to_update.append(Nomenclature(UID=uid, **product))

    update_items = 0
    create_items = []
    if to_create:
        create_items = Nomenclature.objects.bulk_create(to_create)
    if to_update:
        update_items = Nomenclature.objects.bulk_update(
            to_update, list(product.keys())
        )
    return FINAL_TEXT.format(len(create_items), update_items)


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

    return update_or_create_from_1c(parsed_data)


def load_nomenclature_images():
    """Загружает изображения для существующей номенклатуры."""

    fixture_path = os.path.join(settings.CORE_FIXTURES, NOM_FIXTURE)
    with open(f'{fixture_path}', 'r', encoding='utf-8') as file:
        parsed_data = json.load(file)

    to_update = []
    for uid, value in parsed_data.items():
        if value[6] != 'Нет Изображения':
            form, imgstr = value[6].split(';base64,')
            ext = form.split('/')[-1]
            decoded_image = base64.b64decode(imgstr)
            filename = f'{uid}.{ext}'
            # Сохраняем полученное изображение
            img_path = os.path.join(
                settings.MEDIA_ROOT,
                settings.MEDIA_NOM,
                filename
            )
            try:
                with open(img_path, 'wb') as output_file:
                    output_file.write(decoded_image)
            except Exception as e:
                print(f'Ошибка при записи изображения: {e}')
            else:
                # Заменим поле с изображением на путь к нему
                value[6] = os.path.relpath(img_path, start=settings.MEDIA_ROOT)
            to_update.append(Nomenclature(UID=uid, image=value[6]))

    items = Nomenclature.objects.bulk_update(to_update, ['image'])
    return f'Установленных картинок: {items}.'
