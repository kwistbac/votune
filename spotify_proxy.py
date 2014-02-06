#!/usr/bin/env python

import sys, cherrypy, time
sys.path.append("spotify-websocket-api")
from spotify_web.friendly import Spotify


sessions = {}


def get_or_create_session(username, password):
    if username in sessions:
        print time.strftime("%d.%m.%Y %H:%M:%S") + " [" + username + "] Session destroyed"
        sessions[username].logout()
        
    spotify = Spotify(username, password)
    if not spotify:
        print "[" + username + "] Login failed"
        return False
    else:
        print time.strftime("%d.%m.%Y %H:%M:%S") + " [" + username + "] Session created"
        sessions[username] = spotify
    
    #if username not in sessions:
        #spotify = Spotify(username, password)

        #if not spotify:
            #print "[" + username + "] Login failed"
            #return False
        #else:
            #print "[" + username + "] Session created"
            #sessions[username] = spotify
    return sessions[username]


def disconnect_sessions():
    for username, session in sessions.items():
        print time.strftime("%d.%m.%Y %H:%M:%S") + " [" + username + "] Session destroyed"
        session.logout()


class SpotifyURIHandler(object):
    def default(self, username=None, password=None, uri=None, action="proxymp3"):
        if uri is None or username is None or password is None:
            raise cherrypy.HTTPError(400, "A paramater was expected but not supplied.")

        spotify = get_or_create_session(username, password)
        if not spotify:
            raise cherrypy.HTTPError(403, "Username or password given were incorrect.")

        track = spotify.objectFromURI(uri)
        if track is None:
            print time.strftime("%d.%m.%Y %H:%M:%S") + " [" + username + "] Not found: " + uri
            raise cherrypy.HTTPError(404, "Could not find a track with that URI.")

        if action == "proxymp3":
            url = track.getFileURL()
            if not url:
                print time.strftime("%d.%m.%Y %H:%M:%S") + " [" + username + "] Failed to fetch track URL: " + uri
                disconnect_sessions()
                raise cherrypy.HTTPError(404, "Could not find a track URL for that URI.")
            
            covers = track.getAlbum().getCovers()
            if "300" in covers:
                url = url + "|" + covers["300"]
            elif "600" in covers:
                url = url + "|" + covers["600"]
            elif "120" in covers:
                url = url + "|" + covers["120"]
            
            print time.strftime("%d.%m.%Y %H:%M:%S") + " [" + username + "] Fetch track URL: " + uri
        elif action == "proxymeta":
            url = track.getFileURL()
            if not url:
                print time.strftime("%d.%m.%Y %H:%M:%S") + " [" + username + "] Failed to fetch track metadata: " + uri
                raise cherrypy.HTTPError(404, "Could not find metadata for that URI.")
            
            print time.strftime("%d.%m.%Y %H:%M:%S") + " [" + username + "] Fetch track metadata: " + uri
        else:
            raise cherrypy.HTTPError(400, "An invalid action was requested.")

        #print time.strftime("%d.%m.%Y %H:%M:%S") + " [" + username + "] Result: " + url
        
        return url

    default.exposed = True

cherrypy.engine.subscribe("exit", disconnect_sessions)
cherrypy.engine.autoreload.unsubscribe()
cherrypy.config.update({"environment": "production"})
cherrypy.quickstart(SpotifyURIHandler())
