import datetime
import os
from django.forms.models import ModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django import forms
from bootstrap3_datetime.widgets import DateTimePicker
from django.template import RequestContext
import qrcode
from mJuke import settings
from mJuke.apps.establishment.qr.models import QrCode
import MySQLdb
import hashlib
import time
from django.views.decorators.cache import never_cache


class qrCodeCreationForm(ModelForm):
    startedOn = forms.DateTimeField(label="Start DateTime",
                                    initial=datetime.datetime.now(),
                                    widget=DateTimePicker(options={'format': 'YYYY-MM-DD HH:MM', "pickTime": True}))
    expiredOn = forms.DateTimeField(label="Expire DateTime",
                                    initial=datetime.datetime.now() + datetime.timedelta(hours=6),
                                    widget=DateTimePicker(options={'format': 'YYYY-MM-DD HH:MM', "pickTime": True}))

    class Meta:
        model = QrCode
        fields = ['startedOn', 'expiredOn', ]


@never_cache
def generateQR(request):
    form = qrCodeCreationForm()
    hasCode = hashlib.sha1(str(time.time())).hexdigest()[:8]
    userHasQrCode = False
    userQR = None

    if QrCode.objects.filter(account=request.user).exists():
        userHasQrCode = True
        userQR = QrCode.objects.filter(account=request.user)

    if 'ok' in request.POST:
        form = qrCodeCreationForm(request.POST)

        if form.is_valid():
            #check if user has already existing qr code
            if userHasQrCode:
                #delete previous qrCode
                prevQr = QrCode.objects.get(account=request.user)
                prevQrPath = os.path.abspath(os.path.realpath(settings.MEDIA_ROOT) + "/qrCodes/" + str(request.user.id) + "_" + prevQr.hasCode + ".jpg")
                os.unlink(prevQrPath)

                #create new qr image
                startedOn = MySQLdb.escape_string(request.POST['startedOn'])
                expiredOn = MySQLdb.escape_string(request.POST['expiredOn'])
                QrCode.objects.filter(account=request.user).update(
                    startedOn=startedOn,
                    expiredOn=expiredOn,
                    createdOn=datetime.datetime.now(),
                    hasCode=hasCode)

            else:
                c = form.save(commit=False)
                c.account = request.user
                c.hasCode = hasCode
                c.save()

            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=5,
                border=4,
            )
            qr.add_data("http://127.0.0.1:8000/" + hasCode)
            qr.make(fit=True)
            img = qr.make_image()
            imagePath = os.path.abspath(
                os.path.realpath(settings.MEDIA_ROOT) + "/qrCodes/" + str(request.user.id) + "_" + hasCode + ".jpg")
            img.save(imagePath)

            if not userHasQrCode:
                return HttpResponse(status=201)

    return render_to_response("establishment/qr/qr.html",
                              {'form': form,
                               'userHasCode': userHasQrCode,
                               'usrQr': userQR},
                              context_instance=RequestContext(request))