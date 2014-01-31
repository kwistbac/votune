from django.conf.urls import patterns, include, url
import votune
from votune.apps.establishment import views
from votune.apps.establishment.qr.views import generateQR

urlpatterns = patterns('',

                       url(r'^$', views.index, name='index'),
                       
                       url(r'^library/', include('votune.apps.establishment.library.urls')),

                       url(r'^player/', include('votune.apps.establishment.player.urls')),

                       url(r'^qr/$', generateQR, name='qr-code'),

                       )
