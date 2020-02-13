from flask import render_template, url_for, flash, redirect, request, Blueprint, jsonify
from multitool import db, bcrypt
from datetime import date, datetime, timedelta
import spotipy
import spotipy.util as util
import json
import yaml
import os

music = Blueprint('music', __name__)

def load_config():
    global user_config
    project_root = os.path.dirname(os.path.dirname(__file__))
    stream = open(project_root + '\spotify_config.yaml')
    user_config = yaml.load(stream)

def spotifyTest():
    scope = 'user-top-read user-read-private user-library-read user-read-recently-played playlist-modify-private playlist-modify-public'
    token = util.prompt_for_user_token(user_config['username'], scope=scope, client_id=user_config['client_id'], client_secret=user_config['client_secret'], redirect_uri=user_config['redirect_uri'])
    if token:
        spotifyObject = spotipy.Spotify(auth=token)
        recent = spotifyObject.current_user_recently_played(limit='5')
        print(json.dumps(recent, indent=2, sort_keys=True))
    else:
        print("No Token found.")

load_config()
#spotifyTest()

@music.route("/spotipy")
def spotipy():
    # golf_rounds = Golf_Round.query.all()
    # golf_courses = Golf_Course.query.all()
    return render_template('spotipy.html', title='Spotipy')