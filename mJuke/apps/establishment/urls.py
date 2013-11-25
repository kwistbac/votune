from django.conf.urls import patterns, include, url
from mJuke.apps.establishment import views

urlpatterns = patterns('',

                       url(r'^$', views.index, name='index'),
                       
                       url(r'^library/', include('mJuke.apps.establishment.library.urls')),

                       url(r'^accounts/login/$', views.login),

                       url(r'^accounts/logout/$', views.logout),

                       url(r'^accounts/edit/$', views.editAccount),
                       
                       )
