from django.db import models


class FiledType(models.Model):
    """
    Модель типов поля
    """
    field = models.CharField(max_length=64, unique=True, verbose_name='Тип поля')

    def __str__(self):
        return self.field

    class Meta:
        verbose_name = 'тип поля тега'
        verbose_name_plural = 'типы полей тегов'


class Tag(models.Model):
    """
    Создаем тег с переменной, ссылкой на тип поля и указанием, является ли тег общим для документов
    """
    name = models.CharField(max_length=128, unique=True, default='', verbose_name='Название тега')
    variable = models.CharField(max_length=64, unique=True, verbose_name='Название переменной тега')
    field_type = models.ForeignKey(FiledType, default='textarea', on_delete=models.SET_DEFAULT, verbose_name='Тип поля')
    is_common = models.BooleanField(verbose_name='Общий', default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'
        ordering = ['name']
