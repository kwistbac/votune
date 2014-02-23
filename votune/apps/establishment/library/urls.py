from django.conf.urls import patterns, url
from votune.apps.establishment.library import views
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',

                       url(r'^$', login_required(views.LibraryListView.as_view()), name='library-list'),

                       url(r'^add$', views.add, name='library-add'),

                       url(r'^addSpotify$', views.addSpotify, name='library-add-spotify'),

                       url(r'^edit/(?P<id>\d+)$', views.edit, name='library-edit'),

                       url(r'^remove/(?P<id>\d+)$', views.remove, name='library-remove'),
                       
                       url(r'^upload$', views.upload, name='library-upload'),
                       
                       url(r'^upload/clean$', views.upload_clean, name='library-upload-clean'),

                       url(r'^upload/(?P<need_to_delete>.*)$', views.upload_delete, name='library-upload-delete'),
                       
                       )
