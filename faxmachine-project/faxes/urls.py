from django.urls import path

from . import views # equivalent to 'from faxes import views'

urlpatterns = [
    path('', views.home, name='home'),
    path('send/', views.send, name='send'),
    path('success/', views.success, name='success'),
]