import spotipy, json, base64
from spotipy.oauth2 import SpotifyOAuth
from datetime import date

def printJson(jsonInput):
    print(json.dumps(jsonInput, indent=2))

def connect():
    global sp, numToAdd, offset
    offset = 0

    # Define songs to add
    numToAdd = 25

    # Define connection info and utils
    scope = 'user-library-read,playlist-read-private,playlist-modify-private,ugc-image-upload,user-read-playback-state,user-modify-playback-state'
    SPOTIPY_CLIENT_ID = 'client_ID'
    SPOTIPY_CLIENT_SECRET = 'client_SECRET'
    SPOTIPY_REDIRECT = 'redirect'

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT))

# Get next 8 user playlists
def loadPlaylists():
    global offset
    data = sp.current_user_playlists(limit=9, offset=offset)['items']
    plFound = False

    pkg = '<div class="pRow">'

    for idx, i in enumerate(data):
        pName = i['name']
        if pName == 'Honeycomb':
            plFound = True
            continue
        if not plFound and idx == 8:
            continue

        pTracks = i['tracks']['total']
        if len(i['images']) != 0:
            pImage = i['images'][0]['url']
        else:
            pImage = 'https://i.scdn.co/image/ab67706c0000bebbbdbfc3cf4bb8e97104191236'
        pID = i['id']

        pkg += '<div class="pCol"><div class="pContainer"><img src="'+pImage+'" class="playlist" style="width:100%"><div class="playlistInfo"><div class="pText">'+pName+'</div><div class="pSubtext">'+str(pTracks)+' <small>tracks</small></div><button class="btn pSelect" onclick="selectPlaylist(\'p'+pID+'\')">Select playlist</button></div></div></div>'
        if idx+1 % 4 == 0 and idx != 0:
            pkg += '</div><div class="pRow">'
    pkg += '</div>'

    offset += 8
    return pkg

def getPlaylist(selectID):
    plName = "Honeycomb"

    # Create/update playlist with 25 most recent songs from target playlist
    global newID
    newID = 0
    recentPlaylists = sp.current_user_playlists(limit=50)['items']

    for playlist in recentPlaylists:
        if playlist['name'] == plName:
            newID = playlist['id']

    desc = "Last updated on " + str(date.today()) + ", pulled from " + sp.playlist(playlist_id=selectID)['name']
    if newID == 0:
        sp.user_playlist_create(user=sp.current_user()['id'], name=plName, public=False, collaborative=False, description=desc)
        newID = sp.current_user_playlists(limit=1)['items'][0]['id']
    else:
        sp.playlist_change_details(playlist_id=newID, description=desc)

    oldSongs = sp.playlist_items(playlist_id=newID, limit=100)['items']
    oldIDs = []
    for idx, i in enumerate(oldSongs):
        oldIDs.append(i['track']['uri'])
    if len(oldSongs) != 0: sp.playlist_remove_all_occurrences_of_items(playlist_id=newID, items=oldIDs)

    selectPlSize = sp.playlist(playlist_id=selectID)['tracks']['total']
    recentSongs = sp.playlist_items(playlist_id=selectID, offset=selectPlSize - numToAdd, limit=numToAdd)['items']
    recentSongsID = []
    for i in recentSongs:
        recentSongsID.append(i['track']['id'])

    sp.playlist_add_items(playlist_id=newID, items=recentSongsID)

    with open('Artboard 2_2.jpg', 'rb') as image:
        imgEnc = base64.b64encode(image.read())
    sp.playlist_upload_cover_image(playlist_id=newID, image_b64=imgEnc)

def playNew():
    devices = sp.devices()['devices']
    if devices == []:
        msg = '<div class="alert alert-warning" role="alert">No device available to play on</div>'
        return msg
    else: device = devices[0]

    for idx, i in enumerate(devices):
        if i['is_active']: device = devices[idx]

    honeyData = sp.playlist(playlist_id=newID)
    sp.start_playback(device_id=device['id'], context_uri=honeyData['uri'])

    return '<div class="alert alert-info" role="alert">Successfully playing on '+device['name']+'</div>'