from flask import render_template, url_for, flash, redirect, request, Blueprint, jsonify
from multitool import db, bcrypt
from datetime import date, datetime, timedelta
import spotipy
import spotipy.util as util
import json
import yaml
import os
from multitool.static.scripts.weeklyTrackPlaylist import run
from multitool.music.utils import get_track_obj

music = Blueprint('music', __name__)

def load_config():
    global user_config
    project_root = os.path.dirname(os.path.dirname(__file__))
    #stream = open(project_root + '\spotify_config.yaml')
    stream = open(project_root + '/spotify_config.yaml')
    user_config = yaml.load(stream, Loader=yaml.FullLoader)

def spotifyTest():
    scope = 'user-top-read user-read-private user-library-read user-read-recently-played playlist-modify-private playlist-modify-public'
    token = util.prompt_for_user_token(user_config['username'], scope=scope, client_id=user_config['client_id'], client_secret=user_config['client_secret'], redirect_uri=user_config['redirect_uri'])
    if token:
        spotifyObject = spotipy.Spotify(auth=token)
        recent = spotifyObject.current_user_recently_played(limit='50')
        #print(json.dumps(recent, indent=2, sort_keys=True))
        return recent
    else:
        print("No Token found.")

load_config()
#spotifyTest()

@music.route("/spotify")
def spotify():
    scope = 'user-top-read user-read-private user-library-read user-read-recently-played playlist-modify-private playlist-modify-public'
    token = util.prompt_for_user_token(user_config['username'], scope=scope, client_id=user_config['client_id'], client_secret=user_config['client_secret'], redirect_uri=user_config['redirect_uri'])
    if token:
        spotifyObject = spotipy.Spotify(auth=token)
        # topArtists = spotifyObject.current_user_top_artists(limit='20')
        topTracksS = spotifyObject.current_user_top_tracks(limit='20', time_range="short_term")
        topTracksM = spotifyObject.current_user_top_tracks(limit='20', time_range="medium_term")
        topTracksL = spotifyObject.current_user_top_tracks(limit='20', time_range="long_term")

        topTracks_Short = []
        for track in topTracksS['items']:
            topTracks_Short.append(get_track_obj(track))
        
        topTracks_Medium = []
        for track in topTracksM['items']:
            topTracks_Medium.append(get_track_obj(track))
        
        topTracks_Long = []
        for track in topTracksL['items']:
            topTracks_Long.append(get_track_obj(track))
                
        return render_template('spotify.html', title='Spotipy', topTracks_Short_Payload=json.dumps(topTracks_Short), topTracks_Short=topTracks_Short, topTracks_Medium=topTracks_Medium, topTracks_Long=topTracks_Long)
    else:
        print("No Token found.")
    

@music.route('/spotify/weeklyTrackPlaylist', methods=['POST', 'GET'])
def weeklyTrackPlaylist():
    run(user_config)
    flash('Synced!', 'success')
    return redirect(url_for('music.spotify'))