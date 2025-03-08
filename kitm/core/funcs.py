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
