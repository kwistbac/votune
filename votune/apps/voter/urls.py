from django.conf.urls import patterns, url
from votune.apps.voter.views import *

urlpatterns = patterns('',

                       #(r'^$', main_index),
                       (r'^(\d{1,3})$', voter_index),
                       (r'^upvote/', voter_upVote),
                       (r'^downvote/', voter_downVote),
                       (r'^songs/$', voter_listSongs),
                       (r'^update/$', voter_update),


                       )