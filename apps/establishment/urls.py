from django.conf.urls import patterns, include, url
from apps.establishment import views

urlpatterns = patterns('',

                       url(r'^$', views.index, name='index'),
                       
                       url(r'^library/', include('apps.establishment.library.urls')),


                       )
