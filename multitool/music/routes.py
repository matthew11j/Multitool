from flask import render_template, url_for, flash, redirect, request, Blueprint, jsonify
from flask_wtf import Form
from multitool import db, bcrypt
from datetime import date, datetime, timedelta
from flask_login import current_user
import spotipy
import spotipy.util as util
import json
import yaml
import os
from multitool.static.scripts.weeklyTrackPlaylist import WTP_run
from multitool.static.scripts.seedSpotipy import Seeds_run, getArtistUri, getSongUri
from multitool.music.utils import get_track_obj
from multitool.music.forms import Recommendation

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

# --------------------------------------
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

        result = spotifyObject.recommendation_genre_seeds()
        # print(json.dumps(result, indent=2, sort_keys=True))
                
        return render_template('spotify.html', title='Spotipy', topTracks_Short_Payload=json.dumps(topTracks_Short), topTracks_Short=topTracks_Short, topTracks_Medium=topTracks_Medium, topTracks_Long=topTracks_Long)
    else:
        print("No Token found.")
    

@music.route('/spotify/weeklyTrackPlaylist', methods=['POST', 'GET'])
def weeklyTrackPlaylist():
    WTP_run(user_config)
    flash('Synced!', 'success')
    return redirect(url_for('music.spotify'))

@music.route("/spotify/recommendations", methods=['POST', 'GET'])
def recommendations():
    form = Recommendation()
    if form.validate_on_submit():
        artist_uris = []
        track_uris = []
        genre_uris = []
        seeds = form.seeds
        for seed in seeds:
            seed_type = seed.seed_select.data
            seed_string = seed.seed_string.data
            if seed_type == 'artist':
                artist_uris.append(getArtistUri(user_config, seed_string))
            elif seed_type == 'song':
                strings = [x.strip() for x in seed_string.split(',')]
                song_name = strings[0]
                if len(strings) > 1:
                    artist_name = strings[1]
                else:
                    artist_name = None

                track_uris.append(getSongUri(user_config, song_name, artist_name))
            elif seed_type == 'genre':
                genre_uris.append(seed_string)
            else: # Empty Seed Row
                uri = None

        print(artist_uris)
        print(track_uris)
        print(genre_uris)
        scope = 'user-top-read user-read-private user-library-read user-read-recently-played playlist-modify-private playlist-modify-public'
        token = util.prompt_for_user_token(user_config['username'], scope=scope, client_id=user_config['client_id'], client_secret=user_config['client_secret'], redirect_uri=user_config['redirect_uri'])
        if token:
            spotifyObject = spotipy.Spotify(auth=token)
            results = spotifyObject.recommendations(seed_artists=artist_uris, seed_tracks=track_uris, seed_genres=genre_uris, target_popularity='90')
            for track in results['tracks']:
                print('%s - %s', track['name'],
                    track['artists'][0]['name'])

        return redirect(url_for('music.recommendations'))
    
    return render_template('recommendations.html', title='Recommendations', form=form)
