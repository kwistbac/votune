from django.conf.urls import patterns, url
from mJuke.apps.establishment.player import views

urlpatterns = patterns('',

                       url(r'^queue$', views.queue, name='player-queue'),

                       url(r'^next$', views.next, name='player-next'),
                       
                       )
