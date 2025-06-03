from django.db import models
from django.conf import settings

import core.constants as constants


class Nomenclature(models.Model):
    name = models.CharField(
        'Наименование',
        max_length=constants.MAX_CHARFIELD,
    )
    UID = models.CharField(
        max_length=36,
        unique=True,
        editable=False,
        primary_key=True
    )
    quantity = models.PositiveSmallIntegerField('Количество')
    text = models.TextField('Описание', max_length=constants.MAX_CHARFIELD)
    price = models.PositiveIntegerField('Цена')
    article = models.CharField(
        'Артикул',
        max_length=constants.MIN_CHARFIELD,
    )
    unit_of_measure = models.CharField(
        'Ед. изм.',
        max_length=constants.MIN_CHARFIELD
    )
    category = models.CharField('Категория', max_length=50)
    on_home = models.BooleanField('На Главной', default=False)
    image = models.ImageField(
        'Изображение',
        upload_to=settings.MEDIA_NOM,
        blank=True)

    class Meta:
        ordering = ('category',)
        db_table = 'nomenclature'
