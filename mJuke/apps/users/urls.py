from django.conf.urls import patterns, url


urlpatterns = patterns('',

                       url(r'^$', 'mJuke.apps.users.views.home'),


                       )