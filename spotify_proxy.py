#!/usr/bin/env python

import sys, cherrypy, time, json
sys.path.append("spotify-websocket-api")
from spotify_web.friendly import Spotify


sessions = {}


def get_or_create_session(username, password, force_create = False):
    if username in sessions:
        # Avoid hammering with invalid login attempts (results in temporary lock out)
        if sessions[username]['current'] == False and sessions[username]['password'] == password:
            print time.strftime("%d.%m.%Y %H:%M:%S") + " [" + username + "] Login failed (cached)"
            return False
        if force_create or sessions[username]['current'] and not sessions[username]['current'].logged_in():
            print time.strftime("%d.%m.%Y %H:%M:%S") + " [" + username + "] Session destroyed"
            if sessions[username]['current']:
                sessions[username]['current'].logout()
            sessions[username]['current'] = None
        
    if username not in sessions or sessions[username]['current'] == None:    
        spotify = Spotify(username, password)
        if not spotify.logged_in():
            print time.strftime("%d.%m.%Y %H:%M:%S") + " [" + username + "] Login failed"
            sessions[username] = { 'current':False, 'password':password }
            return False
    
        print time.strftime("%d.%m.%Y %H:%M:%S") + " [" + username + "] Session created"
        sessions[username] = { 'current':spotify, 'password':password }
    
    return sessions[username]['current']


def disconnect_sessions():
    for username, session in sessions.items():
        print time.strftime("%d.%m.%Y %H:%M:%S") + " [" + username + "] Session destroyed"
        session['current'].logout()


class SpotifyURIHandler(object):
    def default(self, username=None, password=None, uri=None, action="proxymp3"):
        if uri is None or username is None or password is None:
            raise cherrypy.HTTPError(400, "A paramater was expected but not supplied.")

        spotify = get_or_create_session(username, password, True)
        if not spotify:
            raise cherrypy.HTTPError(403, "Username or password given were incorrect.")
        track = spotify.objectFromURI(uri)
            
        if track is None:
            print time.strftime("%d.%m.%Y %H:%M:%S") + " [" + username + "] Not found: " + uri
            raise cherrypy.HTTPError(404, "Could not find a track with that URI.")

        if action == "track":
            result = {'url':track.getFileURL(), 'image':None}
            
            if not result['url']:
                print time.strftime("%d.%m.%Y %H:%M:%S") + " [" + username + "] Failed to fetch track URL: " + uri
                raise cherrypy.HTTPError(404, "Could not find a track URL for that URI.")
            
            covers = track.getAlbum().getCovers()
            if "300" in covers:
                result['image'] = covers["300"]
            elif "600" in covers:
                result['image'] = covers["600"]
            elif "120" in covers:
                result['image'] = covers["120"]
            
            print time.strftime("%d.%m.%Y %H:%M:%S") + " [" + username + "] Fetch track URL: " + uri
        elif action == "meta":
            result = {'title':track.getName(), 'artist':track.getArtists(True), 'length':track.getDuration()/1000, 'album':track.getAlbum(True), 'track':track.getNumber()}
            
            if not result['title']:
                print time.strftime("%d.%m.%Y %H:%M:%S") + " [" + username + "] Failed to fetch track metadata: " + uri
                raise cherrypy.HTTPError(404, "Could not find metadata for that URI.")
                
            print time.strftime("%d.%m.%Y %H:%M:%S") + " [" + username + "] Fetch track metadata: " + uri
        else:
            raise cherrypy.HTTPError(400, "An invalid action was requested.")

        #print time.strftime("%d.%m.%Y %H:%M:%S") + " [" + username + "] Result: " + url
        
        return json.dumps(result)

    default.exposed = True

cherrypy.engine.subscribe("exit", disconnect_sessions)
cherrypy.engine.autoreload.unsubscribe()
cherrypy.config.update({"environment": "production"})
cherrypy.quickstart(SpotifyURIHandler())
