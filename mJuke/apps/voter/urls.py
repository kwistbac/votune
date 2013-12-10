from django.conf.urls import patterns, url
from mjuke.apps.voter.views import *

urlpatterns = patterns('',

                       (r'^voter/(\d{1,3})$', voter_index),
                       (r'^voter/upvote/(\d{1,3})$', voter_upVote),
                       (r'^voter/downvote/(\d{1,3})$', voter_downVote),
                       (r'^voter/songs/$', voter_listSongs),
                       (r'^voter/songs/popular/$', voter_listPopularSongs),
                       (r'^voter/about/$', voter_about),
                       (r'^voter/help/$', voter_help),
                       (r'^voter/suggest/$', voter_suggest),


                       )