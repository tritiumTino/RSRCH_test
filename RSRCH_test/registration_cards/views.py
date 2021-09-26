from django.shortcuts import render, HttpResponse
from .models import RegistrationCard


def confirm(request, signature):
    """
    Подтверждение оферты
    """
    reg_card = RegistrationCard.objects.get(signature=signature)
    reg_card.is_approved = True
    if reg_card.is_refused:
        reg_card.is_refused = False
    reg_card.save()
    return render(request, 'registration_cards/answer.html', context={'answer': 1})


def refuse(request, signature):
    """
    Отказ от оферты
    """
    reg_card = RegistrationCard.objects.get(signature=signature)
    reg_card.is_refused = True
    if reg_card.is_approved:
        reg_card.is_approved = False
    reg_card.save()
    return render(request, 'registration_cards/answer.html', context={'answer': 0})
