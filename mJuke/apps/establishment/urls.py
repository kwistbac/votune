from django.conf.urls import patterns, include, url
import mJuke
from mJuke.apps.establishment import views
from mJuke.apps.establishment.playlist.views import playlist

urlpatterns = patterns('',

                       url(r'^$', views.index, name='index'),
                       
                       url(r'^library/', include('mJuke.apps.establishment.library.urls')),

                       url(r'^playlist/$', playlist),
                       )
