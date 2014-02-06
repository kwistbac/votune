from xmlrpclib import DateTime
import datetime
from django.db import models
from votune.models import Account


class QrCode(models.Model):
    account = models.OneToOneField(Account)
    createdOn = models.DateTimeField(default=datetime.datetime.now())
    startedOn = models.DateTimeField()
    expiredOn = models.DateTimeField()
    hasCode = models.CharField(max_length=100)
