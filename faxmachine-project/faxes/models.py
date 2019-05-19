from django.db import models

class SentFax(models.Model):
    date = models.DateTimeField()
    recipient = models.CharField(max_length=12)
    document = models.FileField(upload_to="sent/")

class RecievedFax(models.Model):
    date = models.DateTimeField()
    sender = models.CharField(max_length=12)
    document = models.FileField(upload_to='inbox/')
