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
