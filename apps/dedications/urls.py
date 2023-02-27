from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name = 'home'),
    path('record/', record, name = 'record'),
    path('edit_occupation/<int:id>', edit_occupation, name = 'edit_occupation'),
    path('delete_occupation/<int:id>', delete_occupation, name = 'delete_occupation')
]