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
from multitool.static.scripts.my_spotify_api import getArtistUri, getSongUri
from multitool.music.utils import get_track_obj, get_artist_uri_from_track, send_recommendation_email
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
                spotifyObject = spotipy.Spotify(auth=token)
                artist_uris = []
                track_uris = []
                genre_uris = []
                seeds = form.seeds
                for seed in seeds:
                    seed_type = seed.seed_select.data
                    seed_string = seed.seed_string.data
                    if seed_type == 'artist':
                        artist_uris.append(getArtistUri(spotifyObject, seed_string))
                    elif seed_type == 'song':
                        strings = [x.strip() for x in seed_string.split(',')]
                        song_name = strings[0]
                        if len(strings) > 1:
                            artist_name = strings[1]
                        else:
                            artist_name = None

                        track_uris.append(getSongUri(spotifyObject, song_name, artist_name))
                    elif seed_type == 'genre':
                        genre_uris.append(seed_string)
                    else: # Empty Seed Row
                        uri = None

                    results = spotifyObject.recommendations(seed_artists=artist_uris, seed_tracks=track_uris, seed_genres=genre_uris, target_popularity='90')
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
        spotifyObject = spotipy.Spotify(auth=token)

        genre_seeds = spotifyObject.recommendation_genre_seeds()
        # print(json.dumps(result, indent=2, sort_keys=True))

        # topTracks = spotifyObject.current_user_top_tracks(limit='20', time_range="short_term")
        topTracks = spotifyObject.current_user_top_tracks(limit='20', time_range="medium_term")
        # topTracks = spotifyObject.current_user_top_tracks(limit='20', time_range="long_term")

        tracks = []
        tracksDisplay = []
        tracksToAdd = []
        count = 0 
        track_display = ''
        # topTracks_Obj = []
        for track in topTracks['items']:
            # topTracks_Obj.append(get_track_obj(track))
            artist_uris = []
            artist_uris.append(get_artist_uri_from_track(track))
            results = spotifyObject.recommendations(seed_artists=artist_uris, target_popularity='90')
            for track in results['tracks']:
                if track['id'] not in tracksToAdd:
                    count=count+1
                    print(count)
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

        # playlistName = 'Automagic Test'
        # description = 'Automagic Test'
        # spotifyObject.user_playlist_change_details(user_config['username'], user_config['weekly_playlist_uri_partial'], name=playlistName, description=description)
        spotifyObject.user_playlist_replace_tracks(user_config['username'], user_config['test_playlist_uri_partial'], tracksToAdd)
        send_recommendation_email(tracksDisplay)
    
    return render_template('recommendations.html', title='Recommendations', form=form, tracks=tracks, genre_seeds=genre_seeds)