from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, HttpResponseForbidden
from django.template import RequestContext
from django.shortcuts import render_to_response, render
from django.contrib import messages

from django.views.generic.list import ListView
from django.views.decorators.csrf import csrf_exempt
from django.forms import ModelForm
from django.utils import timezone

from mJuke.models import Song
from mJuke.models import Account

from mJuke import settings
from mJuke.libs.file_uploader import qqFileUploader

from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3

import os
import shutil


class LibraryListView(ListView):
    template_name = 'establishment/library/list.html'
    model = Song

    def render_to_response(self, context, **kwargs):
        if self.request.user.id:
            account = Account.objects.get(user_id=self.request.user.id)
            for folder in ['upload', 'chunks', 'library']:
                path = os.path.join(settings.MEDIA_ROOT, folder + "/" + str(account.id) + "/")
                if not os.path.isdir(path):
                    os.makedirs(path)
        return super(LibraryListView, self).render_to_response(context, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(LibraryListView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class LibraryForm(ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'artist', 'album', 'track', 'year', 'genre', 'comment']

    def __init__(self, *args, **kwargs):
        super(LibraryForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


def add(request):
    try:
        account = Account.objects.get(user_id=request.user.id)
    except:
        return HttpResponseForbidden()

    if 'ok' in request.POST:
        uploadPath = os.path.join(settings.MEDIA_ROOT, "upload/" + str(account.id) + "/")
        libraryPath = os.path.join(settings.MEDIA_ROOT, "library/" + str(account.id) + "/")

        for file in os.listdir(uploadPath):
            name = file.split('_', 1)

            audio = MP3(uploadPath + file)
            song = Song(account_id=account.id,
                        title=audio.tags["TIT2"].text[0] if 'TIT2' in audio.tags and audio.tags['TIT2'].text[0] else
                        name[1],
                        artist=audio.tags['TPE1'].text[0] if 'TPE1' in audio.tags and audio.tags['TPE1'].text[
                            0] else "Uknown artist",
                        length=audio.info.length,
                        album=audio.tags['TALB'].text[0] if 'TALB' in audio.tags else "",
                        track=audio.tags['TRCK'].text[0] if 'TRCK' in audio.tags else None,
                        year=audio.tags['TDRC'].text[0].get_text() if 'TDRC' in audio.tags else None,
                        genre=audio.tags['TCON'].text[0] if 'TCON' in audio.tags else "",
                        comment=audio.tags['COMM'].text[0] if 'COMM' in audio.tags else "")
            song.save()

            os.rename(uploadPath + file, libraryPath + str(song.id) + ".mp3")
        return HttpResponse(status=201)

    return render_to_response('establishment/library/add.html', {}, context_instance=RequestContext(request))


@csrf_exempt
def upload(request):
    try:
        account = Account.objects.get(user_id=request.user.id)
    except:
        return HttpResponseForbidden()

    uploader = qqFileUploader(request, os.path.join(settings.MEDIA_ROOT, "upload/" + str(account.id) + "/"), [".mp3"],
                              2147483648)
    return HttpResponse(uploader.handleUpload())


@csrf_exempt
def upload_delete(request, need_to_delete):
    try:
        account = Account.objects.get(user_id=request.user.id)
    except:
        return HttpResponseForbidden()

    qqFileUploader.UPLOAD_DIRECTORY = os.path.join(settings.MEDIA_ROOT, "upload/" + str(account.id) + "/")
    qqFileUploader.deleteFile(need_to_delete)
    return HttpResponse("ok")


@csrf_exempt
def upload_clean(request):
    try:
        account = Account.objects.get(user_id=request.user.id)
    except:
        return HttpResponseForbidden()

    uploadPath = os.path.join(settings.MEDIA_ROOT, "upload/" + str(account.id) + "/")
    for file in os.listdir(uploadPath):
        os.unlink(uploadPath + file)

    chunksPath = os.path.join(settings.MEDIA_ROOT, "chunks/" + str(account.id) + "/")
    for dir in os.listdir(chunksPath):
        shutil.rmtree(chunksPath + dir)

    return HttpResponse("ok")


def edit(request, id):
    try:
        account = Account.objects.get(user_id=request.user.id)
    except:
        return HttpResponseForbidden()
    try:
        song = Song.objects.get(pk=id)
    except:
        return HttpResponseNotFound()

    if 'ok' in request.POST:
        form = LibraryForm(request.POST, instance=song)
        if form.is_valid():
            form.save()
            return HttpResponse(status=201)
    else:
        form = LibraryForm(instance=song)

    return render_to_response('establishment/library/edit.html', {"form": form},
                              context_instance=RequestContext(request))


def remove(request, id):
    try:
        account = Account.objects.get(user_id=request.user.id)
    except:
        return HttpResponseForbidden()
    try:
        song = Song.objects.get(pk=id)
    except:
        return HttpResponseNotFound()

    libraryPath = os.path.join(settings.MEDIA_ROOT, "library/" + str(account.id) + "/")

    if 'ok' in request.POST:
        if os.path.isfile(libraryPath + str(song.id) + ".mp3"):
            os.unlink(libraryPath + str(song.id) + ".mp3")
        song.delete()
        return HttpResponse(status=201)

    return render_to_response('establishment/library/remove.html', {"song": song},
                              context_instance=RequestContext(request))
