from django.conf.urls import patterns, url
from mJuke.apps.establishment.library import views

urlpatterns = patterns('',

                       url(r'^$', views.LibraryListView.as_view(), name='library'),

                       url(r'^add$', views.add, name='library-add'),

                       url(r'^edit/(?P<id>\d+)$', views.edit, name='library-edit'),

                       url(r'^remove/(?P<id>\d+)$', views.remove, name='library-remove'),
                       
                       url(r'^upload$', views.upload, name='library-upload'),
                       
                       url(r'^upload/clean$', views.upload_clean, name='library-upload-clean'),

                       url(r'^upload/(?P<need_to_delete>.*)$', views.upload_delete, name='library-upload-delete'),
                       
                       )
