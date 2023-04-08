from datetime import date

import base64
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import spotipy.util as util

class PlaylistManager:

    def __init__(self):
        self.sp = None
        self.numToAdd = 25
        self.offset = 0
        self.our_playlist_id = 0

    @staticmethod
    def print_json(jsonInput):
        print(json.dumps(jsonInput, indent=2))

    def connect(self):
        # Define connection info and utils
        scope = 'user-library-read,playlist-read-private,playlist-modify-private,ugc-image-upload,user-read-playback-state,user-modify-playback-state'
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    # Get next 8 user playlists
    def load_playlists(self):
        data = self.sp.current_user_playlists(limit=9, offset=self.offset)['items']
        playlist_found = False

        pkg = '<div class="pRow">'

        for idx, i in enumerate(data):
            playlist_name = i['name']
            if playlist_name == 'Honeycomb':
                playlist_found = True
                continue
            if not playlist_found and idx == 8:
                continue

            playlist_tracks = i['tracks']['total']
            if len(i['images']) != 0:
                playlist_img = i['images'][0]['url']
            else:
                playlist_img = 'https://i.scdn.co/image/ab67706c0000bebbbdbfc3cf4bb8e97104191236'
            playlist_id = i['id']

            pkg += '<div class="pCol"><div class="pContainer"><img src="' + playlist_img + '" class="playlist" style="width:100%"><div class="playlistInfo"><div class="pText">' + playlist_name + '</div><div class="pSubtext">' + str(
                playlist_tracks) + ' <small>tracks</small></div><button class="btn pSelect" onclick="selectPlaylist(\'p' + playlist_id + '\')">Select playlist</button></div></div></div>'
            if idx + 1 % 4 == 0 and idx != 0:
                pkg += '</div><div class="pRow">'
        pkg += '</div>'

        self.offset += 8
        return pkg

    def get_playlist(self, selectID):
        playlist_name = "Honeycomb"

        # Create/update playlist with 25 most recent songs from target playlist
        self.our_playlist_id = 0
        recent_playlists = self.sp.current_user_playlists(limit=50)['items']

        for playlist in recent_playlists:
            if playlist['name'] == playlist_name:
                self.our_playlist_id = playlist['id']

        desc = "Last updated on " + str(date.today()) + ", pulled from " + self.sp.playlist(playlist_id=selectID)[
            'name']
        if self.our_playlist_id == 0:
            self.sp.user_playlist_create(user=self.sp.current_user()['id'], name=playlist_name, public=False,
                                         collaborative=False,
                                         description=desc)
            self.our_playlist_id = self.sp.current_user_playlists(limit=1)['items'][0]['id']
        else:
            self.sp.playlist_change_details(playlist_id=self.our_playlist_id, description=desc)

        old_songs = self.sp.playlist_items(playlist_id=self.our_playlist_id, limit=100)['items']
        old_ids = []
        for idx, i in enumerate(old_songs):
            old_ids.append(i['track']['uri'])
        if len(old_songs) != 0: self.sp.playlist_remove_all_occurrences_of_items(playlist_id=self.our_playlist_id,
                                                                                 items=old_ids)

        playlist_size = self.sp.playlist(playlist_id=selectID)['tracks']['total']
        recent_songs = \
            self.sp.playlist_items(playlist_id=selectID, offset=playlist_size - self.numToAdd, limit=self.numToAdd)[
                'items']
        recent_song_ids = []
        for i in recent_songs:
            recent_song_ids.append(i['track']['id'])

        self.sp.playlist_add_items(playlist_id=self.our_playlist_id, items=recent_song_ids)

        with open('Artboard 2_2.jpg', 'rb') as image:
            img_base64 = base64.b64encode(image.read())
        self.sp.playlist_upload_cover_image(playlist_id=self.our_playlist_id, image_b64=img_base64)

    def play_new(self):
        devices = self.sp.devices()['devices']
        if not devices:
            msg = '<div class="alert alert-warning" role="alert">No device available to play on</div>'
            return msg
        else:
            device = devices[0]

        for idx, i in enumerate(devices):
            if i['is_active']: device = devices[idx]

        honey_data = self.sp.playlist(playlist_id=self.our_playlist_id)
        self.sp.start_playback(device_id=device['id'], context_uri=honey_data['uri'])

        return '<div class="alert alert-info" role="alert">Successfully playing on ' + device['name'] + '</div>'
