import spotipy
from spotipy.oauth2 import SpotifyOAuth
from conf import *

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=clientId,
                                               client_secret=clientSecret,
                                               redirect_uri=redirectUrl,
                                               scope="playlist-modify-private playlist-modify-public"))
for transfer in transfers:
    uris = []
    for src in transfer['src']:
        playlist = sp.playlist(playlist_id=src)
        for track in playlist['tracks']['items']:
            uris.append(track['track']['uri'])

    for target in transfer['target']:
        sp.playlist_add_items(playlist_id=target, items=uris)
