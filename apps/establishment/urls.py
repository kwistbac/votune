from django.conf.urls import patterns, include, url
from apps.establishment import views

urlpatterns = patterns('',

                       url(r'^$', views.index, name='index'),
                       
                       url(r'^library/', include('apps.establishment.library.urls')),

                       url(r'^accounts/login/$', 'apps.establishment.views.login'),

                       url(r'^accounts/logout/$', 'apps.establishment.views.logout'),

                       url(r'^accounts/edit/$', 'apps.establishment.views.editAccount'),

                       )
