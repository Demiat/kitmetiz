from django.db import models

from . import constants


class Nomenclature(models.Model):
    name = models.CharField(
        'Наименование',
        max_length=constants.MAX_CHARFIELD,
        editable=False)
    UID = models.CharField(
        max_length=36,
        unique=True,
        editable=False)
    quantity = models.PositiveSmallIntegerField('Количество')
    text = models.TextField('Описание', max_length=constants.MAX_CHARFIELD)
    price = models.PositiveIntegerField('Цена')
    article = models.CharField(
        'Артикул',
        max_length=constants.MIN_CHARFIELD,
        editable=False)
    unit_of_measure = models.CharField(
        'Единица Измерения',
        max_length=constants.MIN_CHARFIELD
    )
    category = models.CharField('Категория', max_length=50)
    on_home = models.BooleanField('На Главной', default=False)
    image = models.ImageField(
        'Изображение',
        upload_to='smedia/nomenclature/',
        blank=True)

    class Meta:
        orderin = ('category',)
