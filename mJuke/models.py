from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Account(models.Model):
    user = models.OneToOneField(User)
    company = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    phone = models.CharField(max_length=50)
    modified = models.DateTimeField(auto_now=True)

    @classmethod
    def getByID(cls, userID):
        return cls.objects.get(user=userID)


class Song(models.Model):
    account = models.ForeignKey(Account)
    queue = models.SmallIntegerField(null=True)
    length = models.PositiveSmallIntegerField(null=True)
    title = models.CharField(max_length=60)
    artist = models.CharField(max_length=60)
    album = models.CharField(max_length=60)
    track = models.PositiveSmallIntegerField(null=True)
    year = models.PositiveSmallIntegerField(null=True)
    genre = models.CharField(max_length=30)
    comment = models.CharField(max_length=60)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class Vote(models.Model):
    account = models.ForeignKey(Account)
    song = models.ForeignKey(Song)
    value = models.SmallIntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)


class Log(models.Model):
    account = models.ForeignKey(Account)
    song = models.ForeignKey(Song)
    created = models.DateTimeField(auto_now_add=True)


class Suggest(models.Model):
    account = models.ForeignKey(Account)
    song = models.ForeignKey(Song)
    title = models.CharField(max_length=60)
    artist = models.CharField(max_length=60)
    album = models.CharField(max_length=60)
    track = models.PositiveSmallIntegerField(null=True)
    year = models.PositiveSmallIntegerField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
