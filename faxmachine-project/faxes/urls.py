from django.urls import path

from . import views # equivalent to 'from faxes import views'

urlpatterns = [
    path('send/', views.send, name='send'),
    path('success/', views.success, name='success'),
    # path('fax_inbound/', views.fax_inbound, name='fax_inbound'),
    # path('fax_recieved/', views.fax_recieved, name='fax_recieved'),
]