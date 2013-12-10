from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from mJuke import settings

admin.autodiscover()
from mJuke.apps.establishment import views
from mJuke import settings

urlpatterns = patterns('',

 
                       url(r'^voter/', include('mJuke.apps.voter.urls')),

                       url(r'^media/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': settings.MEDIA_ROOT,}),
                       
                       url(r'^establishment/', include("mJuke.apps.establishment.urls")),

                       url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       url(r'^admin/', include(admin.site.urls)),

                       url(r'^accounts/login/', views.login),

                       url(r'^accounts/logout/', views.logout),

                       url(r'^accounts/edit/', views.editAccount),

                       url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
                           {'document_root': settings.MEDIA_ROOT}),

)
