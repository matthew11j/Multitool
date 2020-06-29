import spotipy
import spotipy.util as util
import json
import yaml
import os
import logging
from flask import render_template, url_for, flash, redirect, request, Blueprint, jsonify
from flask_wtf import Form
from multitool import db, bcrypt
from datetime import date, datetime, timedelta
from flask_login import current_user
from multitool.static.scripts.weekly_track_playlist import WTP_run
from multitool.static.scripts.my_spotify_api import get_artist_uri, get_song_uri
from multitool.music.utils import get_track_obj, get_artist_uri_from_track, send_recommendation_email
from multitool.music.forms import Recommendation

music = Blueprint('music', __name__)
logging.basicConfig(filename='multitool.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %I:%M:%S %p')
logger = logging.getLogger('Multitool')

def load_config():
    global user_config
    project_root = os.path.dirname(os.path.dirname(__file__))
    #stream = open(project_root + '\spotify_config.yaml')
    stream = open(project_root + '/spotify_config.yaml')
    user_config = yaml.load(stream, Loader=yaml.FullLoader)

def spotify_test():
    scope = 'user-top-read user-read-private user-library-read user-read-recently-played playlist-modify-private playlist-modify-public'
    token = util.prompt_for_user_token(user_config['username'], scope=scope, client_id=user_config['client_id'], client_secret=user_config['client_secret'], redirect_uri=user_config['redirect_uri'])
    if token:
        spotify_object = spotipy.Spotify(auth=token)
        recent = spotify_object.current_user_recently_played(limit='50')
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
        spotify_object = spotipy.Spotify(auth=token)
        # topArtists = spotify_object.current_user_top_artists(limit='20')
        topTracksS = spotify_object.current_user_top_tracks(limit='20', time_range="short_term")
        topTracksM = spotify_object.current_user_top_tracks(limit='20', time_range="medium_term")
        topTracksL = spotify_object.current_user_top_tracks(limit='20', time_range="long_term")

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
    

@music.route('/spotify/weeklTrackPlaylist', methods=['POST', 'GET'])
def weekly_track_playlist():
    WTP_run(user_config)
    flash('Synced!', 'success')
    return redirect(url_for('music.spotify'))

@music.route("/spotify/recommendations", methods=['POST', 'GET'])
def recommendations():
    form = Recommendation()
    tracks = []
    # if request.method == 'POST':
    if form.validate_on_submit():
        if 'add_row' in request.form:
            try:
                form.seeds.append_entry([])
            except:
                pass
            
        elif 'submit' in request.form:
            scope = 'user-top-read user-read-private user-library-read user-read-recently-played playlist-modify-private playlist-modify-public'
            token = util.prompt_for_user_token(user_config['username'], scope=scope, client_id=user_config['client_id'], client_secret=user_config['client_secret'], redirect_uri=user_config['redirect_uri'])
            if token:
                spotify_object = spotipy.Spotify(auth=token)
                artist_uris = []
                track_uris = []
                genre_uris = []
                seeds = form.seeds
                for seed in seeds:
                    seed_type = seed.seed_select.data
                    seed_string = seed.seed_string.data
                    if seed_type == 'artist':
                        artist_uris.append(get_artist_uri(spotify_object, seed_string))
                    elif seed_type == 'song':
                        strings = [x.strip() for x in seed_string.split(',')]
                        song_name = strings[0]
                        if len(strings) > 1:
                            artist_name = strings[1]
                        else:
                            artist_name = None

                        track_uris.append(get_song_uri(spotify_object, song_name, artist_name))
                    elif seed_type == 'genre':
                        genre_uris.append(seed_string)
                    else: # Empty Seed Row
                        uri = None

                # pre_defined_kwargs = {'target_acousticness': 0.90, 'target_popularity': 80}
                pre_defined_kwargs = {'target_popularity': 80}

                results = spotify_object.recommendations(seed_artists=artist_uris, seed_tracks=track_uris, seed_genres=genre_uris, limit=100, **pre_defined_kwargs)
                for track in results['tracks']:
                    tracks.append(get_track_obj(track))
                    print(track['name'] + ' - ' +
                        track['artists'][0]['name'])

                return render_template('recommendations.html', title='Recommendations', form=form, tracks=tracks)

    return render_template('recommendations.html', title='Recommendations', form=form)


@music.route("/spotify/test", methods=['POST', 'GET'])
def test():
    form = Recommendation()
    scope = 'user-top-read user-read-private user-library-read user-read-recently-played playlist-modify-private playlist-modify-public'
    token = util.prompt_for_user_token(user_config['username'], scope=scope, client_id=user_config['client_id'], client_secret=user_config['client_secret'], redirect_uri=user_config['redirect_uri'])
    if token:
        spotify_object = spotipy.Spotify(auth=token)

        genre_seeds = spotify_object.recommendation_genre_seeds()
        # print(json.dumps(result, indent=2, sort_keys=True))

        
        # topTracks = spotify_object.current_user_top_tracks(limit='20', time_range="medium_term")
        # topTracks = spotify_object.current_user_top_tracks(limit='20', time_range="long_term")
        ranges = ["short_term", "medium_term", "long_term"]

        # for loop

        tracks = []
        tracksDisplay = []
        tracksToAdd = []
        count = 0 
        track_display = ''
        # topTracks_Obj = []
        for time_range in ranges:
            topTracks = spotify_object.current_user_top_tracks(limit='20', time_range=time_range)
            for track in topTracks['items']:
                # topTracks_Obj.append(get_track_obj(track))
                artist_uris = []
                artist_uris.append(get_artist_uri_from_track(track))
                results = spotify_object.recommendations(seed_artists=artist_uris, target_popularity='90')
                for track in results['tracks']:
                    if track['id'] not in tracksToAdd:
                        count=count+1
                        track_display = track['name'] + ' - ' + track['artists'][0]['name']
                        if count < 99:
                            tracksToAdd.append(track['id'])
                            tracks.append(get_track_obj(track))
                            tracksDisplay.append(track_display)
                        else:
                            print('Track Over 100!!')
                        print(track_display)
                    else:
                        print('Track Skipped!!')
                        print(track_display)
                    print('---------------')
                    
        # playlistName = 'Automagic Test'
        # description = 'Automagic Test'
        # spotify_object.user_playlist_change_details(user_config['username'], user_config['weekly_playlist_uri_partial'], name=playlistName, description=description)
        spotify_object.user_playlist_replace_tracks(user_config['username'], user_config['test_playlist_uri_partial'], tracksToAdd)
        send_recommendation_email(tracksDisplay)
    
    return render_template('recommendations.html', title='Recommendations', form=form, tracks=tracks, genre_seeds=genre_seeds)