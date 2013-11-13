from django.conf.urls import patterns, url
from apps.establishment.library import views

urlpatterns = patterns('',

                       url(r'^$', views.LibraryListView.as_view(), name='library'),

                       url(r'^add$', views.add, name='library-add'),

                       url(r'^edit/(?P<id>\d+)$', views.edit, name='library-edit'),

                       url(r'^remove/(?P<id>\d+)$', views.remove, name='library-remove'),
                       
                       )
