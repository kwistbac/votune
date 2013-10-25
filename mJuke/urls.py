from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

                       url(r'^$', include('apps.users.urls')),

                       url(r'^establishment/$', include('apps.establishment.urls')),

                       url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       url(r'^admin/', include(admin.site.urls)),


                       )
