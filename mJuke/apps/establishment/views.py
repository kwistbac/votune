# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, render
from django.contrib import messages
from django.conf import settings
import os.path, time

def index(request):
    #ts = time.time()
    ts = os.path.getmtime(settings.STATIC_ROOT + "js/panel.js")
    return render_to_response('establishment/index.html', { "ts": ts })