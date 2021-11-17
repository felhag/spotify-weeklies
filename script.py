import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import date
from conf import *

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=clientId,
                                               client_secret=clientSecret,
                                               redirect_uri=redirectUrl,
                                               open_browser=False,
                                               scope="playlist-modify-private playlist-modify-public playlist-read-private"))

playlists = sp.current_user_playlists()['items']


def find_playlist(username, name, onlyown):
    for playlist in playlists:
        owner = playlist['owner']['id']
        if owner != username and (onlyown or owner != 'spotify'):
            continue

        if playlist['name'].lower() == name.lower():
            return playlist


def find_or_create_playlist(username, name):
    today = date.today()
    fullname = f'{name} {today.year}'
    existing = find_playlist(username, fullname, True)
    if existing:
        return existing

    print(f'creating new playlist for {username}: {fullname}')
    return sp.user_playlist_create(username, fullname, False, False, f'Alle {name.lower()} sinds {date.today().strftime("%d-%m-%Y")}')


def run():
    for transfer in transfers:
        username = transfer['username']
        sources = transfer['src']
        targets = transfer['target']
        uris = []

        for src in sources:
            srcpl = find_playlist(username, src, False)
            if srcpl is None:
                print(f'Could not find {src} for {username}')
                continue

            tracks = sp.playlist(playlist_id=srcpl['id'])['tracks']['items']
            for track in tracks:
                uris.append(track['track']['uri'])

        print(f'found {str(len(uris))} tracks in {str(len(sources))} playlists')
        if len(uris) == 0:
            continue

        for target in targets:
            targetpl = find_or_create_playlist(username, target)
            sp.playlist_add_items(playlist_id=targetpl['id'], items=uris)

        print(f'added {str(len(uris))} tracks to {str(len(targets))} playlists')

    print('Done!')


run()
