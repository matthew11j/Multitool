from flask import render_template, url_for, flash, redirect, request, Blueprint, jsonify
from multitool import db, bcrypt
from datetime import date, datetime, timedelta
import spotipy
import spotipy.util as util
import json
import yaml
import os
from multitool.static.scripts.weeklyTrackPlaylist import run

music = Blueprint('music', __name__)

def load_config():
    global user_config
    project_root = os.path.dirname(os.path.dirname(__file__))
    #stream = open(project_root + '\spotify_config.yaml')
    stream = open(project_root + '/spotify_config.yaml')
    user_config = yaml.load(stream)

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
    recentSongs = spotifyTest()
    recentTracks = []
    for item in recentSongs['items']:
        Dict = {}
        name = item['track']['name']
        Dict['name'] = name
        recentTracks.append(Dict)
    
    #print(json.dumps(recentTracks, indent=2, sort_keys=True))
    return render_template('spotipy.html', title='Spotipy', recentSongs=recentSongs, recentTracksData=json.dumps(recentTracks), recentTracks=recentTracks)

@music.route('/spotify/weeklyTrackPlaylist', methods=['POST', 'GET'])
def weeklyTrackPlaylist():
    run(user_config)
    flash('Synced!', 'success')
    return redirect(url_for('music.spotify'))