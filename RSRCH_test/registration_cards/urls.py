from django.urls import path
from .views import confirm, refuse

app_name = 'registration_cards'

urlpatterns = [
    path('confirm/<str:signature>/', confirm, name='confirm'),
    path('refuse/<str:signature>/', refuse, name='confirm'),
]
