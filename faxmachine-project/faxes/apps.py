"""config for faxes app"""
from django.apps import AppConfig
from django.conf import settings

import firebase_admin
from firebase_admin import credentials

class FaxesConfig(AppConfig):
    name = 'faxes'

    def ready(self):
        firebase_admin.initialize_app(credentials.Certificate(settings.FIREBASE_KEYS), {'storageBucket': settings.FIREBASE_STORAGE_BUCKET})
