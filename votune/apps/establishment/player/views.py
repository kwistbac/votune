from django.shortcuts import render_to_response, render
from django.template import Context, RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

from votune.models import Song, Account
from votune import settings

import requests
import json
import os

def get_current_song(account):
    try:
        current = Song.objects.get(queue = 0, account = account)
    except ObjectDoesNotExist:
        current = Song.objects.filter(account = account).exclude(queue = None).order_by('-queue').first()
        if current != None:
            current.queue = 0
            current.save()
        else:
            current = Song.objects.filter(queue = None, account = account).order_by('?').first()
            if current != None:
                current.queue = 0
                current.save()
    return current

def get_queued_songs(account):
    # Fetch voted songs
    length = 15
    songs = list(Song.objects.filter(queue__gt = 0, account = account).order_by('-queue')[:length])
    diff = length - len(songs)
    if diff == 0:
        # Remove all generated songs
        Song.objects.filter(queue__lt = 0, account = account).update(queue = None)
    else:
        # Fetch generated songs
        offset = 0
        generated = list(Song.objects.filter(queue__lt = 0, account = account).order_by('-queue')[:diff])
        for song in generated:
            offset -= 1
            if song.queue != offset:
                song.queue = offset
                song.save()
            songs.append(song)
        if len(generated) == diff:
            # Remove all superfluous generated songs
            remove = Song.objects.filter(queue__lt = 0, account = account).order_by('-queue')[diff:]
            for song in remove:
                song.queue = None
                song.save()
        else:
            # Add list of generated random songs
            add = list(Song.objects.filter(queue = None, account = account).order_by('?')[:(diff - len(generated))])
            for song in add:
                offset -= 1        
                song.queue = offset
                song.save()
                songs.append(song)
    return songs

@login_required
def queue(request):
    try:
        account = Account.objects.get(user_id = request.user.id)
    except:
        return HttpResponseNotFound()

    result = {'queue': []}
        
    queue = get_queued_songs(account)
    for song in queue:
        result['queue'].append(model_to_dict(song))
    
    return HttpResponse(json.dumps(result), content_type="application/json")

@login_required
def current(request):
    try:
        account = Account.objects.get(user_id = request.user.id)
    except:
        return HttpResponseNotFound()

    result = {'current':None, 'queue': []}
    
    current = get_current_song(account)
    if current != None:
        result['current'] = model_to_dict(current)
        
        if current.source == Song.SOURCE_SPOTIFY:
            if len(account.spotify_username) == 0 or len(account.spotify_password) == 0:
                return next(request)
            query = {'uri': 'spotify:track:' + current.hash, 'username': account.spotify_username, 'password': account.spotify_password}
            try:
                url = requests.get("http://localhost:8080/", params=query)
            except:
                return next(request)
            result['current']['url'] = url.text
        else:
            result['current']['url'] = settings.MEDIA_URL + "library/" + str(account.id) + "/" + str(current.id) + ".mp3"
        
        imagePath = "library/" + str(account.id) + "/" + str(current.id) + ".jpg"
        if os.path.isfile(os.path.join(settings.MEDIA_ROOT, imagePath)):
            result['current']['image'] = settings.MEDIA_URL + imagePath
    
    queue = get_queued_songs(account)
    for song in queue:
        result['queue'].append(model_to_dict(song))
    
    return HttpResponse(json.dumps(result), content_type="application/json")

@login_required
def next(request):
    try:
        account = Account.objects.get(user_id = request.user.id)
    except:
        return HttpResponseNotFound()
    
    song = get_current_song(account)
    if song != None:
        song.queue = None
        song.save()
    
    return current(request)