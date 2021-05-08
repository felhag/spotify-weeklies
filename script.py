import spotipy
from spotipy.oauth2 import SpotifyOAuth
from conf import *

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=clientId,
                                               client_secret=clientSecret,
                                               redirect_uri=redirectUrl,
                                               open_browser=False,
                                               scope="playlist-modify-private playlist-modify-public"))
for transfer in transfers:
    sources = transfer['src']
    targets = transfer['target']
    uris = []

    for src in sources:
        playlist = sp.playlist(playlist_id=src)
        for track in playlist['tracks']['items']:
            uris.append(track['track']['uri'])

    print(f'found {str(len(uris))} tracks in {str(len(sources))} playlists')

    for target in targets:
        sp.playlist_add_items(playlist_id=target, items=uris)

    print(f'added {str(len(uris))} tracks to {str(len(targets))} playlists')

print('Done!')
