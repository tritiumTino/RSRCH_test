from .models import get_text_content
from django.core.mail import send_mail
from django.template.loader import get_template


def data_create(instance, current_card, fio, email, offer_term):
    """
    Формируем данные на основе тегов, регистрационной карточки и электронного документа
    """
    template = replace_info(instance, current_card, fio, email, offer_term)
    template = eval(template)
    context = generate_document_data(template, current_card)
    return context


def replace_info(instance, current_card, fio, email, offer_term):
    """
    Подставляем данные в шаблон
    :param instance: объект класса EDocument
    :param current_card: объект класса RegistrationCard
    :param fio: ФИО
    :param email: Email
    :param offer_term: Offer term
    :return:
    """
    template = str(get_text_content(instance.template))
    data = {
        '%id_doc%': str(instance.id_doc),
        '%id_doc_date%': str(instance.value_set.get(tags__variable='%id_doc_date%').value_of),
        '%date%': str(instance.value_set.get(tags__variable='%date%').value_of),
        '%send_date%': str(instance.value_set.get(tags__variable='%send_date%').value_of),
        '%reg_doc%': str(current_card.reg_doc),
        '%regcard%': current_card.signature,
        '%reg_doc_date%': f'{current_card.reg_doc_date:%Y.%m.%d %H:%M}',
        '%fio%': fio,
        '%email%': email,
        '%offer_term%': offer_term,
        '%key%': str(current_card.key),
        '%signature%': current_card.signature
    }
    for key in data:
        template = template.replace(key, data[key])
    return template


def generate_document_data(template, current_card):
    """
    Формируем контекст для отправки письма
    :param template: шаблон с подставленными значениями
    :param current_card: регистрационная карточка
    :return: словарь с контекстом
    """
    str_meta = template['Метаинформация документа']
    str_content = template['Содержание документа']
    str_conditions = template['Условия обмена документом']
    str_rules = template['Правила признания договоренностей, согласования условий']
    str_requisites = template['Реквизиты документа']
    str_requisites_with_data = template['Реквизиты документа с персональными данными']
    signature = current_card.signature

    return {
        'str_meta': str_meta,
        'str_content': str_content,
        'str_conditions': str_conditions,
        'str_rules': str_rules,
        'str_requisites': str_requisites,
        'str_requisites_with_data': str_requisites_with_data,
        'signature': signature
    }


def send_file_mail(document, context, email):
    """
    Отправляем письмо пользователю
    :param document: регистрационнная карточка
    :param context: словарь с контекстом
    :param email: Email
    :return: None
    """
    doc_name = str(document.doc_content.doc_name)
    send_mail(
        subject=doc_name,
        from_email='email_from',
        message=doc_name,
        recipient_list=(email, ),
        fail_silently=True,
        html_message=get_template('registration_cards/confirmation.html').render(context)
    )
