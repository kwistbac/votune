from django.conf.urls import patterns, url


urlpatterns = patterns('',

                       url(r'^$', 'apps.establishment.views.home'),


                       )
