import json
from flask_mail import Message
from multitool import mail

def get_track_obj(track):
    Dict = {}
    name = track['name']
    images = track['album']['images']
    artist = track['artists'][0]
    popularity = track['popularity']
    Dict['name'] = name
    Dict['images'] = images
    Dict['artist'] = artist
    Dict['popularity'] = popularity
    return Dict

def get_artist_uri_from_track(track):
    return track['artists'][0]['id']


def send_recommendation_email(payload):
    msg = Message(subject='Recommended Songs Playlist',
                  sender='noreply@demo.com',
                  recipients=['matthew011j@gmail.com'])
    msg.body = f'''This is a list of songs recommended from the test:
{json.dumps(payload, indent=2, sort_keys=True)}
'''
    mail.send(msg)
