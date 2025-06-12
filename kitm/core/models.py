from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


from core.constants import MAX_CHARFIELD, MIN_CHARFIELD
from users.models import User

MAX_LENGTH_NAME = 30


class Nomenclature(models.Model):
    """Номенклатура."""

    name = models.CharField(
        'Наименование',
        max_length=MAX_CHARFIELD,
    )
    UID = models.CharField(
        max_length=36,
        unique=True,
        editable=False,
        primary_key=True
    )
    quantity = models.PositiveSmallIntegerField('Количество')
    text = models.TextField('Описание', max_length=MAX_CHARFIELD)
    price = models.PositiveIntegerField('Цена')
    article = models.CharField(
        'Артикул',
        max_length=MIN_CHARFIELD,
    )
    unit_of_measure = models.CharField(
        'Ед. изм.',
        max_length=MIN_CHARFIELD
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
        verbose_name = 'Номенклатура'
        verbose_name_plural = 'Номенклатура'

    def __str__(self):
        return self.name[:MAX_LENGTH_NAME]


class Rating(models.Model):
    """Рейтинг для номеклатуры."""

    nomenclature = models.ForeignKey(
        Nomenclature,
        on_delete=models.CASCADE,
        verbose_name='Номенклатура'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    rating = models.PositiveSmallIntegerField(
        verbose_name='Рейтинг',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )

    class Meta:
        verbose_name = 'Рейтинг номенклатуры'
        verbose_name_plural = 'Рейтинг номенклатуры'
        default_related_name = '%(model_name)ss'
        ordering = ('rating',)
        db_table = 'rating'
        constraints = (
            models.UniqueConstraint(
                fields=('nomenclature', 'author'),
                name='unique_rating'
            ),
        )

    def __str__(self):
        return f'{self.nomenclature.name[:MAX_LENGTH_NAME]}: {self.rating}'
