# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.template import loader, Context
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, HttpResponseForbidden
from mJuke.apps.establishment.qr.models import QrCode
from mJuke.models import *
from django.contrib import auth
from django.shortcuts import render_to_response
from django.template import Context, RequestContext
from django.http import HttpResponseRedirect
from mJuke.SearchService import *
import datetime
from django.utils.timezone import utc


def main_index(request, hashCode):
    if QrCode.objects.filter(hasCode=hashCode).exists():
        qrObj = QrCode.objects.get(hasCode=hashCode)
        qrExprDateTime = qrObj.expiredOn
        if qrExprDateTime <= datetime.datetime.utcnow().replace(tzinfo=utc):
            return HttpResponse("QR code has expired.")
        else:
            return voter_index(request, qrObj.account_id)
    else:
        return HttpResponse("Hash Value not found")

def voter_index(request,accountId):

    try:
        request.session['account_id'] = accountId
        account = Account.objects.get(id = accountId)
    except:
        return HttpResponseNotFound()

    playList = Song.objects.filter(account=account).exclude(queue=0).order_by('-queue')[:15]
    nowPlaying = Song.objects.filter(queue=0, account=account)

    return render_to_response('voter/index.html',{'playlist' : playList,'nowplaying': nowPlaying, 'accountId': accountId}, context_instance=RequestContext(request))


def voter_listSongs(request):

    try:
        accountId = request.session['account_id']
        account = Account.objects.get(id = accountId)
    except:
        return HttpResponseNotFound()

    if request.method =="POST" and request.POST.get('srch-query') != "":

        query = request.POST.get('srch-query')
        songList = SearchService.SearchMusicLibrary(query,account)
        return render_to_response('voter/songs.html',{'songlist' : songList,'accountId': accountId}, context_instance=RequestContext(request))

    else:

        songList = Song.objects.filter(account = account)
        return render_to_response('voter/songs.html',{'songlist' : songList,'accountId': accountId}, context_instance=RequestContext(request))


def voter_listPopularSongs(request):

    'Have we thought about how popular songs are defined?'

    try:
        accountId = request.session['account_id']
        account = Account.objects.get(id = accountId)
        songList = Song.objects.filter(account = account)
    except:
        return HttpResponseNotFound()

    return render_to_response('voter/songs.html',{'songlist' : songList, 'accountId': accountId}, context_instance=RequestContext(request))


def voter_about(request):

    return render_to_response('voter/about.html',{'accountId':request.session['account_id']}, context_instance=RequestContext(request))

def voter_help(request):

    return render_to_response('voter/help.html',{'accountId': request.session['account_id']}, context_instance=RequestContext(request))


def voter_upVote(request,songId):

    vote(request, songId, 1)
    return HttpResponseRedirect('/voter/%s' % request.session['account_id'])


def voter_downVote(request,songId):

    vote(request, songId, -1)
    return HttpResponseRedirect('/voter/%s' % request.session['account_id'])

def vote(request,songId,amount):

    try:
        song = Song.objects.get(id=songId)

        if song.queue < 0 and amount > 0:
            song.queue = 0 + amount
        elif song.queue < 0 and amount <= 0:
            song.queue = None
        elif song.queue is None and amount > 0:
            song.queue = amount
        elif song.queue is None and amount <= 0:
            song.queue = None
        elif (song.queue + amount) <= 0:
            song.queue = None
        else:
            song.queue += amount

        account = Account.objects.get(id = request.session['account_id'])
        vote = Vote(song = song, account = account, value= amount)
        song.save()
        vote.save()

    except:
        return HttpResponseForbidden()


def voter_suggest(request):
    try:
        accountId = request.session['account_id']
    except:
        return HttpResponseForbidden()

    if  request.method == 'POST':

        account = Account.objects.get(id = accountId)
        title = request.POST.get('title', '')
        artist = request.POST.get('artist', '')
        album = request.POST.get('album', '')
        suggestion = Suggest(title = title, artist = artist, album= album, account = account)
        suggestion.save()

        return HttpResponseRedirect('/voter/%s' % accountId)

    else:

        return render_to_response('voter/suggest.html',{'accountId': accountId}, context_instance=RequestContext(request))


