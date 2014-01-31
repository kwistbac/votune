from xmlrpclib import DateTime
import datetime
from django.db import models
from django.contrib.auth.models import User


class QrCode(models.Model):
    account = models.OneToOneField(User)
    createdOn = models.DateTimeField(default=datetime.datetime.now())
    startedOn = models.DateTimeField()
    expiredOn = models.DateTimeField()
    hasCode = models.CharField(max_length=100)
