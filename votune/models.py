from django.db import models
from django.contrib.auth.models import User
#from django.db.models.signals import post_save

class Account(models.Model):
    user = models.OneToOneField(User)
    company = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    phone = models.CharField(max_length=50)
    spotify_username = models.CharField(max_length=50, blank=True)
    spotify_password = models.CharField(max_length=50, blank=True)
    modified = models.DateTimeField(auto_now=True)

    @classmethod
    def getByID(cls, userID):
        return cls.objects.get(user=userID)


class Song(models.Model):
    SOURCE_FILE = 0
    SOURCE_SPOTIFY = 1
    SOURCES = ((SOURCE_FILE, 'File'), (SOURCE_SPOTIFY, 'Spotify'))
    
    account = models.ForeignKey(Account)
    source = models.SmallIntegerField(choices=SOURCES, default=SOURCE_FILE)
    hash = models.CharField(max_length=32)
    queue = models.SmallIntegerField(null=True, blank=True)
    length = models.PositiveSmallIntegerField(null=True)
    title = models.CharField(max_length=60)
    artist = models.CharField(max_length=60)
    album = models.CharField(max_length=60, blank=True)
    track = models.PositiveSmallIntegerField(null=True, blank=True)
    year = models.PositiveSmallIntegerField(null=True, blank=True)
    genre = models.CharField(max_length=30, blank=True)
    comment = models.CharField(max_length=60, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ("account", "source", "hash")

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


