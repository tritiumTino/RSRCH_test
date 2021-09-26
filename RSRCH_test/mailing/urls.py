from django.urls import path
from .views import index


app_name = 'mailing'

urlpatterns = [
    path('', index, name='index'),
]
