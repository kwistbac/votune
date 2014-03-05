# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.forms import model_to_dict
from django.template import loader, Context
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, HttpResponseForbidden
from votune.apps.establishment import qr
from votune.apps.establishment.qr.models import QrCode
from votune.models import *
from django.contrib import auth
from django.shortcuts import render_to_response
from django.template import Context, RequestContext
from django.http import HttpResponseRedirect
from votune.SearchService import *
import datetime
from django.utils.timezone import utc
import json
from django.views.decorators.csrf import csrf_exempt


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

    message = ''
    if not 'votune_lvt' in request.session :
        set_voter_cookie(request)
        message = "Welcome to Votune. You will be eligible to vote in the next round. The next round will begin in approximately 3 minutes"

    #try:
    request.session['account_id'] = accountId
    #except:
        #return HttpResponseNotFound()
    return render_to_response('voter/index.html',{'message' : message}, context_instance=RequestContext(request))


def voter_listSongs(request):

    try:
        accountId = request.session['account_id']
        account = Account.objects.get(id = accountId)
    except:
        return HttpResponseNotFound()

    if request.method =="POST" and request.POST.get('srch-query') != "":

        query = request.POST.get('srch-query')
        songList = SearchService.SearchMusicLibrary(query,account)

    else:

        songList = Song.objects.filter(account = account)


    return render_to_response("voter/voterSearch.html",{'object_list': songList,'query': query, 'ableToVote': isAbleToVote(request) },context_instance=RequestContext(request))



def voter_upVote(request):

    if request.method == 'POST' and isAbleToVote(request):
        songId = request.POST['songId']
        vote(request, songId, 1)
        set_voter_cookie(request)
        
    return voter_update(request)


def voter_downVote(request):

    if request.method == 'POST' and isAbleToVote(request):
        songId = request.POST['songId']
        vote(request, songId, -1)
        set_voter_cookie(request)

    return voter_update(request)

def vote(request,songId,amount):

    #try:
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

    #except:
        #return HttpResponseForbidden()

@csrf_exempt
def voter_update(request):

    try:
        account = Account.objects.get(id = request.session['account_id'])
    except:
        return HttpResponseNotFound()

    result = {'current':None, 'queue': [], 'ableToVote': None}
    current = Song.objects.get(queue=0, account=account)
    result['current'] = model_to_dict(current)

    if isAbleToVote(request) :
        result['ableToVote'] = True
    else :
        result['ableToVote'] = False

    queue = Song.objects.filter(account=account).exclude(queue=0).order_by('-queue')[:15]
    for song in queue:
        result['queue'].append(model_to_dict(song))

    return HttpResponse(json.dumps(result), content_type="application/json")

def set_voter_cookie(request):

    DateTime = datetime.datetime.now().strftime("%y-%m-%d-%H-%M-%S")
    request.session['votune_lvt'] = DateTime

def isAbleToVote(request):

    if 'votune_lvt' in request.session :
        LastVoted = datetime.datetime.strptime(request.session['votune_lvt'], "%y-%m-%d-%H-%M-%S")
        TimeBetweenVotes = datetime.datetime.now() - LastVoted

        if TimeBetweenVotes >= datetime.timedelta(seconds = 10) :
            return True
        else :
            return False
    else :
        set_voter_cookie()
        return False

