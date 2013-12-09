from django.db.models import Q
from models import *

class SearchService(object):

    @classmethod
    def SearchMusicLibrary(cls, query, account):
        #improved search algorithm implementation if needed
        songList = Song.objects.filter(Q(account=account) & Q(title__icontains=query) | Q(artist__icontains=query))
        return songList


