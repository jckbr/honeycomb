import os
from datetime import date

import base64
from io import BytesIO

import PIL
import requests
import spotipy
from spotipy import FlaskSessionCacheHandler, CacheFileHandler
from spotipy.oauth2 import SpotifyOAuth
from PIL import Image

PLAYLIST_NAME = 'Honeycomb'


class PlaylistManager:

    def __init__(self):
        self.sp = None  # Spotify object
        self.numToAdd = 10  # Number of songs to add to Honeycomb playlist
        self.offset = 0  # Offset for loading playlists
        self.our_playlist_id = 0  # ID of Honeycomb playlist
        self.user_num_of_playlists = 0  # Number of user playlists
        self.user_playlists = None  # List of user playlists

        self.cache = {}  # Cache for Spotify token
        self.cache_manager = FlaskSessionCacheHandler(self.cache)  # Cache manager for Spotify token;

        self.playlist_img = None  # Image of Honeycomb playlist
        self.placeholder_img = None  # Placeholder image for playlists without images

        self.create_base64_imgs()

    def create_base64_imgs(self):
        with open(os.path.join(os.getcwd(), 'static', 'imgs', 'logo_orange.jpg'), 'rb') as image:
            # generate html base64 image
            self.playlist_img = base64.b64encode(image.read()).decode('utf-8')

        with open(os.path.join(os.getcwd(), 'static', 'imgs', 'logo_big.png'), 'rb') as image:
            self.placeholder_img = base64.b64encode(image.read()).decode('utf-8')

    def connect(self):
        # Define connection info and utils
        scope = 'user-library-read,playlist-read-private,playlist-modify-private,ugc-image-upload,user-read-playback-state,user-modify-playback-state'
        self.offset = 0
        # Use FlaskSessionCacheHandler to cache token
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, cache_handler=self.cache_manager))
        self.user_playlists = self.sp.current_user_playlists()['items']
        # remove all playlists with less than self.numToAdd songs
        self.user_playlists = [i for i in self.user_playlists if i['tracks']['total'] >= self.numToAdd]
        # remove honeycomb playlist from list
        self.user_playlists = [i for i in self.user_playlists if i['name'] != PLAYLIST_NAME]

    # Get next 8 user playlists
    def load_playlists(self):
        if self.offset >= len(self.user_playlists):
            self.offset = 0

        pkg = '<div class="pRow">'

        for playlist in self.user_playlists[self.offset:self.offset + 8]:
            playlist_tracks = playlist['tracks']['total']
            playlist_name = playlist['name']
            if len(playlist['images']) != 0:
                playlist_img = playlist['images'][0]['url']
                # if height and width are none, resize to 640x640
                if playlist['images'][0]['height'] is None and playlist['images'][0]['width'] is None:
                    # use PIL to resize image
                    try:
                        playlist_img = playlist['images'][0]['url']
                        # use pillow to resize image
                        img = Image.open(requests.get(playlist_img, stream=True).raw)
                        img = img.resize((640, 640))
                        # convert to base64
                        buffered = BytesIO()
                        img.save(buffered, format="JPEG")
                        encoded_string = base64.b64encode(buffered.getvalue())
                        playlist_img = 'data:image/jpeg;base64,' + encoded_string.decode('utf-8')
                    except PIL.UnidentifiedImageError:
                        playlist_img = playlist['images'][0]['url']
            else:
                playlist_img = self.placeholder_img
            playlist_id = playlist['id']

            pkg += """
                <div class="pCol">
                    <div class="pContainer">
                        <img src=" """ + playlist_img + """ " class="playlist" style="width:100%">
                        <div class="playlistInfo">
                            <div class="pText"> 
                                """ + playlist_name + """ 
                            </div>
                            <div class="pSubtext"> 
                                """ + str(playlist_tracks) + """ 
                                <small>
                                    tracks
                                </small>
                            </div>
                            <button class="btn pSelect" onclick="selectPlaylist(\'p""" + playlist_id + """\')">
                                Select playlist    
                            </button>
                        </div>
                    </div>
                </div>
            """

            # if we have 4 playlists, start a new row
            if self.user_playlists.index(playlist) % 4 == 3:
                pkg += '</div><div class="pRow">'

            # if we have less than 4 playlists, add empty divs
            if self.user_playlists.index(playlist) == len(self.user_playlists) - 1:
                if len(self.user_playlists) % 4 == 1:
                    pkg += '<div class="pCol"></div><div class="pCol"></div><div class="pCol"></div>'
                elif len(self.user_playlists) % 4 == 2:
                    pkg += '<div class="pCol"></div><div class="pCol"></div>'
                elif len(self.user_playlists) % 4 == 3:
                    pkg += '<div class="pCol"></div>'

        self.offset += 8

        pkg += '</div>'

        return pkg

    def get_playlist(self, select_id):

        # Create/update playlist with 25 most recent songs from target playlist
        recent_playlists = self.sp.current_user_playlists(limit=50)['items']

        # Find playlist ID
        pulled_playlist = [playlist['id'] for playlist in recent_playlists if playlist['name'] == PLAYLIST_NAME]

        desc = "Last updated on " + str(date.today()) + ", pulled from " + self.sp.playlist(playlist_id=select_id)[
            'name']

        if len(pulled_playlist) == 1:
            self.our_playlist_id = pulled_playlist[0]
            self.sp.playlist_change_details(playlist_id=self.our_playlist_id, description=desc)
        else:
            self.sp.user_playlist_create(user=self.sp.current_user()['id'], name=PLAYLIST_NAME, public=False,
                                         collaborative=False,
                                         description=desc)
            self.our_playlist_id = self.sp.current_user_playlists(limit=1)['items'][0]['id']

        old_songs = self.sp.playlist_items(playlist_id=self.our_playlist_id, limit=self.numToAdd)['items']

        if len(old_songs) != 0:
            # only get spotify ids if the playlist is not empty
            old_ids = [spotify_id['track']['uri'] for spotify_id in old_songs]
            self.sp.playlist_remove_all_occurrences_of_items(playlist_id=self.our_playlist_id, items=old_ids)

        playlist_size = self.sp.playlist(playlist_id=select_id)['tracks']['total']

        # find the most recent songs and add them to our playlist
        self.sp.playlist_add_items(playlist_id=self.our_playlist_id, items=[str(track['track']['id']) for track in
                                                                            self.sp.playlist_items(
                                                                                playlist_id=select_id,
                                                                                offset=playlist_size - self.numToAdd,
                                                                                limit=self.numToAdd)['items']])

        self.sp.playlist_upload_cover_image(playlist_id=self.our_playlist_id, image_b64=self.playlist_img)

    def play_new(self):
        devices = self.sp.devices()['devices']
        if not devices:
            msg = '<div class="alert alert-warning" role="alert">No device available to play on</div>'
            return msg
        else:
            device = devices[0]

        device = next((d for d in devices if d['is_active']), devices[0])

        self.sp.start_playback(device_id=device['id'], context_uri=self.sp.playlist(playlist_id=self.our_playlist_id)['uri'])

        return '<div class="alert alert-info" role="alert">Successfully playing on ' + device['name'] + '</div>'
