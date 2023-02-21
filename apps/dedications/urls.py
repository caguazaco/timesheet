from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name = 'home'),
    path('record/', record, name = 'record'),
    path('delete_occupation/<int:id>', delete_occupation, name='delete_occupation')
]