import json
import base64
import os

from django.conf import settings

from . models import Nomenclature

JSON_FIXTURE = '123.json'


def process_exchange_1C():
    """Обмен данными с 1С."""
    fixture_path = os.path.join(settings.CORE_FIXTURES, JSON_FIXTURE)
    with open(f'{fixture_path}', 'r', encoding='utf-8') as file:
        parsed_data = json.load(file)
    # Обходим структуру
    for uid in parsed_data:
        product = dict(
            name=uid[0],
            quantity=uid[1],
            price=uid[2],
            article=uid[3],
            unit_of_measure=uid[4],
            category=uid[5],
            image=uid[6],
        )
        if product['image'] != 'Нет Изображения':
            # image_base64_bytes = product['image'].encode('ascii')
            # decoded_image = base64.b64decode(image_base64_bytes)
            form, imgstr = product['image'].decode().split(';base64,')
            ext = form.split('/')[-1]
            decoded_image = base64.b64decode(imgstr)
            filename = f'{uid}.{ext}'
            # Сохраняем полученное изображение
            img_path = os.path.join(settings.MEDIA_NOM, filename)
            with open(img_path, 'wb') as output_file:
                output_file.write(decoded_image)
                # Заменим поле с изображением на путь к нему
                product['image'] = img_path
        else:
            product['image'] = None

        to_create = []
        to_update = []
        uids = set(Nomenclature.objects.values_list('UID', flat=True))
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
    return (
        f'Создано {len(create_items)}, обновлено {len(update_items)} записей!'
    )
