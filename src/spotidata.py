import os
import io
import sys
import json
import urllib.request

from datetime import datetime

import spotipy


class SpotifyData:
    def __init__(self, sptObj=None):
        self.spotifyObject = sptObj
        if sptObj:
            self.data_dict = self.fetchData(sptObj)
        else:
            print('empty SpotifyObject')
            self.spotifyObject = self.auth()

    def auth(self):
        if os.path.isfile('creds.json') and os.access('creds.json', os.R_OK):
            print('USING EXISTING CREDS')
            f = open('creds.json')
            creds = json.load(f)
            client_id = creds['client_id']
            client_secret = creds['client_secret']
            f.close()

            redirect_uri = 'http://127.0.0.1:5000'
            scope = 'user-read-private user-read-playback-state user-modify-playback-state user-read-recently-played'
            auth = spotipy.oauth2.SpotifyOAuth(client_id,
                                               client_secret,
                                               redirect_uri,
                                               scope=scope,
                                               open_browser=True)
            spotifyObject = spotipy.Spotify(oauth_manager=auth)

            return spotifyObject
        else:
            print('NO CRED FILE')
            with io.open(os.path.join('creds.json'), 'w') as db_file:
                db_file.write(
                    json.dumps({
                        'client_id': 'ENTER CLIENT ID HERE',
                        'client_secret': 'ENTER CLIENT SECRET HERE'
                    }))
            print("'creds.json' has been created, enter your credentials")
            quit()

    def fetchData(self, spotifyObject):
        # WARNING spoti_dict crashing when changed from spotify
        play_state = 'play'
        lastPlayed = spotifyObject.current_user_recently_played(1)
        online = False
        try:
            self.track = spotifyObject.current_user_playing_track()

            if self.track != None:
                artist = self.track['item']['artists'][0]['name']
                trackName = self.track['item']['name']
                albumName = self.track['item']['album']['name']

                title = trackName + ' - ' + artist + ' - ' + albumName

                album_art = self.track['item']['album']['images'][0]['url']
                cover_data = urllib.request.urlopen(album_art).read()
                # context=ssl.create_default_context(cafile=certifi.where())

                # toggle states
                pb = spotifyObject.current_playback()
                if pb:
                    toggle_states = [pb['shuffle_state'], pb['repeat_state']]
                else:
                    toggle_states = [False, False]

                # DEVICE
                devices = spotifyObject.devices()
                for x in devices['devices']:
                    if x['is_active']:
                        self.active_deviceID = x['id']
                        online = True

                if self.track['is_playing']:
                    play_state = 'pause'
                else:
                    play_state = 'play'
            else:
                raise Exception('currentTrack Error')

            data_dict = {
                'play_state': play_state,
                'lastPlayed': lastPlayed,
                'title': title,
                'cover_data': cover_data,
                'toggle_states': toggle_states,
                'online': online
            }
            return data_dict
        
        except Exception as err:
            artist = lastPlayed['items'][0]['track']['artists'][0]['name']
            trackName = lastPlayed['items'][0]['track']['name']
            albumName = lastPlayed['items'][0]['track']['album']['name']
            title = trackName + ' - ' + artist + ' - ' + albumName

            album_art = lastPlayed['items'][0]['track']['album']['images'][0][
                'url']
            cover_data = urllib.request.urlopen(album_art).read()
            toggle_states = [False, 'off']
            self.online = False
            
            print(f'---{err} Handled---')
            # self.logger(err)
            
            data_dict = {
                'play_state': play_state,
                'lastPlayed': lastPlayed,
                'title': title,
                'cover_data': cover_data,
                'toggle_states': toggle_states,
                'online': online
            }
            return data_dict

    # BUTTON FUNCTIONS

    def play_pauseB(self):
        try:
            if self.track['is_playing']:
                self.spotifyObject.pause_playback(self.active_deviceID)
            else:
                self.spotifyObject.start_playback(self.active_deviceID)
        except Exception as exp:
            self.logger(str(exp))

    def nextB(self):
        try:
            self.spotifyObject.next_track(self.active_deviceID)
        except Exception as exp:
            self.logger(str(exp))

    def prevB(self, ):
        try:
            self.spotifyObject.previous_track(self.active_deviceID)
        except Exception as exp:
            self.logger(str(exp))

    def shuff(self, tog):
        self.spotifyObject.shuffle(tog)

    def repeat(self, tog):
        self.spotifyObject.repeat(tog)

    # LOGGING

    def logger(self, log_message):
        # IDEA json logger
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        error_message = f'{str(exc_type)} {str(file)} {str(exc_tb.tb_lineno)}\n{log_message}'
        # print(error_message)
        with open('log.txt', 'a') as log_file:
            log_file.write(
                f'{datetime.now().strftime("%d-%m-%Y %H:%M")}--{error_message}\n\n'
            )

    # pyuic5 -x spotimini.ui -o uiTest.py
