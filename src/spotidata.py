import os
from os import kill, name
import spotipy
import spotipy.util as util
import urllib.request
import glob

#spotify developer account info
#client_id = "enter your cli id"
#client_secret = "enter your cli secret"
#redirect_uri = "enter your uri"

try:
    cacheRead = glob.glob('.cache-*')
    username = cacheRead[0][7:]
except:
    print('Go to https://www.spotify.com/tr/account/overview/ to get username')
    username = input('Enter your username: ')

scope = 'user-read-private user-read-playback-state user-modify-playback-state user-read-recently-played'

token = util.prompt_for_user_token(
    username, scope, client_id, client_secret, redirect_uri)
if token:
    spotifyObject = spotipy.Spotify(auth=token)
else:
    print("Can't get token for", username)
    kill


def fetchData():
    # CURRENT TRACK

    global track
    global online
    global artist
    global title
    global cover_data
    global play_state
    global toggle_states

    play_state = 'play'

    # current track
    track = spotifyObject.current_user_playing_track()
    if track != None:
        artist = track['item']['artists'][0]['name']
        trackName = track['item']['name']
        albumName = track['item']['album']['name']

        title = trackName + " - " + artist + " - " + albumName

        album_art = track['item']['album']['images'][0]['url']
        cover_data = urllib.request.urlopen(album_art).read()

        # toggle states
        pb = spotifyObject.current_playback()
        toggle_states = [pb['shuffle_state'], pb['repeat_state']]

        # DEVICE
        devices = spotifyObject.devices()
        for x in devices['devices']:
            if x['is_active']:
                global active_deviceID
                active_deviceID = x['id']
                online = True

        if track['is_playing']:
            play_state = 'pause'
        else:
            play_state = 'play'
    else:
        lastPlayed = spotifyObject.current_user_recently_played(1)
        artist = lastPlayed['items'][0]['track']['artists'][0]['name']
        trackName = lastPlayed['items'][0]['track']['name']
        albumName = lastPlayed['items'][0]['track']['album']['name']
        title = trackName + " - " + artist + " - " + albumName

        album_art = lastPlayed['items'][0]['track']['album']['images'][0]['url']
        cover_data = urllib.request.urlopen(album_art).read()
        toggle_states = [False, 'off']
        online = False

# BUTTON FUNCTIONS


def play_pauseB():
    if online:
        try:
            if track['is_playing']:
                spotifyObject.pause_playback(active_deviceID)
            else:
                spotifyObject.start_playback(active_deviceID)
        except:
            print(spotipy.SpotifyException)


def nextB():
    if online:
        try:
            spotifyObject.next_track(active_deviceID)
        except:
            print(spotipy.SpotifyException)


def prevB():
    if online:
        try:
            spotifyObject.previous_track(active_deviceID)
        except:
            print(spotipy.SpotifyException)


def shuff(tog):
    if online:
        spotifyObject.shuffle(tog)


def repeat(tog):
    if online:
        spotifyObject.repeat(tog)
