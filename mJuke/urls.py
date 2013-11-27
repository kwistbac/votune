from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from mJuke.apps.establishment import views

urlpatterns = patterns('',

                       url(r'^$', include('mJuke.apps.users.urls')),

                       url(r'^establishment/', include("mJuke.apps.establishment.urls")),

                       url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       url(r'^admin/', include(admin.site.urls)),

                       url(r'^accounts/login/', views.login),

                       url(r'^accounts/logout/', views.logout),

                       url(r'^accounts/edit/', views.editAccount),

                       )
