from django.conf.urls import patterns, include, url
import mJuke
from mJuke.apps.establishment import views
from mJuke.apps.establishment.playlist.views import playlist
from mJuke.apps.establishment.qr.views import generateQR, qrCode

urlpatterns = patterns('',

                       url(r'^$', views.index, name='index'),
                       
                       url(r'^library/', include('mJuke.apps.establishment.library.urls')),

                       url(r'^playlist/$', playlist),

                       url(r'^qr/$', generateQR),

                       url(r'^qrcode/$', qrCode),
                       )
