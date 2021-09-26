from django.db import models
from documents.models import EDocument
from random import randint
from hashlib import sha1
from documents.utils import get_text_content
from django.db.models.signals import post_save
from django.dispatch import receiver
from .utils import data_create, send_file_mail


class RegistrationCard(models.Model):
    """
    Регистрационная карточка формируется автоматически при создании электронного документа.
    Перед сохранением карточки обновляются поля получателя, уникального ключа и подписи.
    Поля is_approved и is_refused показывают состояние подтверждения/опровержения принятия оферты.
    """
    reg_doc = models.BigAutoField(primary_key=True, verbose_name='Регистрационный номер документа')
    reg_doc_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации документа')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления документа')
    receiver = models.CharField(max_length=256, verbose_name='Получатель', default='')
    doc_content = models.ForeignKey(EDocument, verbose_name='Файл для рассылки', on_delete=models.CASCADE,
                                    related_name='documents')
    key = models.BigIntegerField(verbose_name='Уникальный ключ', blank=True)
    signature = models.CharField(max_length=256, verbose_name='Электронная подпись', blank=True)
    is_approved = models.BooleanField(default=False, verbose_name='Согласовано')
    is_refused = models.BooleanField(default=False, verbose_name='Отказано')

    def save(self, *args, **kwargs):
        """
        Перед сохранением карточки определяем уникальный ключ и электронную подпись к документу
        """
        if not self.key:
            self.key = randint(1, 10000000)
            self.signature = sha1(str(get_text_content(self.doc_content.template)).encode('utf-8')
                                  + str(self.key).encode('utf-8')).hexdigest()
        super(RegistrationCard, self).save()

    def __str__(self):
        return f'{self.doc_content.doc_name}: {self.receiver}'

    class Meta:
        verbose_name = 'Регистрационная карта'
        verbose_name_plural = 'Регистрационные карты'
        ordering = ['-updated_at']


@receiver(post_save, sender=EDocument)
def create_reg_card(sender, instance, **kwargs):
    """
    После создания электронного документа автоматически создаем регистрационные карточки и рассылаем
    письма с подставленными значениями
    :param sender: класс EDocument
    :param instance: экземляр класса EDocument, созданный электронный документ
    """
    send_list = instance.send_list.replace('"', '').split('; ')
    if send_list:
        for receiver in send_list:
            receiver = receiver.split(', ')
            fio, email, offer_term = receiver[0], receiver[1], receiver[2]
            current_card, created = RegistrationCard.objects.get_or_create(doc_content=instance, receiver=fio)
            if not created:
                current_card.doc_content = instance
                current_card.save()
            context = data_create(instance, current_card, fio, email, offer_term)
            send_file_mail(current_card, context, email)
