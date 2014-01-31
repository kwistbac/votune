from django.conf.urls import patterns, url
from votune.apps.establishment.player import views

urlpatterns = patterns('',

                       url(r'^queue$', views.queue, name='player-queue'),
                       
                       url(r'^current', views.current, name='player-current'),

                       url(r'^next$', views.next, name='player-next'),
                       
                       )
