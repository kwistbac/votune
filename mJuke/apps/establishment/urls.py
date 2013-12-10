from django.conf.urls import patterns, include, url
import mJuke
from mJuke.apps.establishment import views
from mJuke.apps.establishment.qr.views import generateQR, qrCode

urlpatterns = patterns('',

                       url(r'^$', views.index, name='index'),
                       
                       url(r'^library/', include('mJuke.apps.establishment.library.urls')),

                       url(r'^player/', include('mJuke.apps.establishment.player.urls')),

                       url(r'^qr/$', generateQR),

                       url(r'^qrcode/$', qrCode),
                       )
