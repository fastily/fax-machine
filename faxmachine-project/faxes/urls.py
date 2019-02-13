from django.urls import path

from . import views # equivalent to 'from faxes import views'

urlpatterns = [
    path('send/', views.send, name='send'),
    path('recieved/', views.recieved, name='recieved'),
]
