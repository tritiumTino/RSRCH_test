from django.db import models
from .utils import get_text_content
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from mailing.models import Tag
from datetime import datetime


class YAMLTemplate(models.Model):
    """
    Загружаем YAML-шаблон
    """
    name = models.CharField(max_length=256, verbose_name='Название шаблона')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата загрузки')
    content = models.FileField(upload_to='media/%Y/%m/%d', verbose_name='Файл шаблона')

    def __str__(self):
        return f'{self.name} - {self.created_at:%Y:%m:%d}'

    class Meta:
        verbose_name = 'Шаблон'
        verbose_name_plural = 'Шаблоны'
        ordering = ['-created_at']


class EDocument(models.Model):
    """
    Класс электронного документа, построенного на шаблоне.
    ID документу присваивается автоматически.
    Перед сохранением документа подтяивается имя документа из соответвующего шаблона.
    Связь с моделью тегов через дополнительую модель Value позволяет присвоить
    тегам соответвующее документу значение.
    """
    id_doc = models.BigAutoField(primary_key=True, verbose_name='Номер документа')
    template = models.ForeignKey(YAMLTemplate, verbose_name='Выбранный шаблон', on_delete=models.CASCADE)
    doc_name = models.CharField(max_length=256, verbose_name='Название документа', default='')
    send_list = models.TextField(verbose_name='Список рассылки',
                                 help_text='Введите информацию в формате "fio, email, offer_term,'
                                           ' пользователей отделять через "; "', default='')
    tags = models.ManyToManyField(Tag, through='Value',
                                  through_fields=('documents', 'tags'))

    def __str__(self):
        return f'{self.id_doc}_{self.doc_name}'

    class Meta:
        verbose_name = 'Электронный документ'
        verbose_name_plural = 'Электронные документы'


@receiver(pre_save, sender=EDocument)
def save_doc_name(sender, instance, **kwargs):
    """
    Подтягиваем имя документа из шаблона и присваиваем соответвующему полю
    """
    text_content = get_text_content(instance.template)
    instance.doc_name = text_content['Реквизиты документа'].split('\n')[1].split(': ')[1]


@receiver(post_save, sender=EDocument)
def set_common_tags(sender, instance, **kwargs):
    """
    После сохранения электронного документа подтягиваем соответвующие общие теги,
    обязательные к заполнению
    """
    instance.tags.set(Tag.objects.filter(is_common=True))


class Value(models.Model):
    """
    Дополнительная модель для присваивания значения тегам документа
    """
    documents = models.ForeignKey(EDocument, on_delete=models.CASCADE, null=True)
    tags = models.ForeignKey(Tag, on_delete=models.CASCADE, null=True)
    value_of = models.DateTimeField(default=datetime.now(), verbose_name='Значение')
