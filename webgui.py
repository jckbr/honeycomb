from flask import Flask, render_template, request, jsonify
from eventlet import wsgi, listen
from flask_cors import CORS
import os
from go_playlist import PlaylistManager
import json

app = Flask(__name__)
CORS(app)
go_obj = PlaylistManager()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/connect')
def web_connect():
    print("Connected")
    go_obj.connect()
    return jsonify(result="1")


@app.route('/loadPlaylists')
def web_load_playlists():
    print("Got playlists")
    data = go_obj.load_playlists()
    return jsonify(result=data)


@app.route('/select')
def web_select():
    # for future reference Jack, id is a reserved word in python (i.e. don't use it)
    playlist_id = request.args.get('plID', 0)
    playlist_id = playlist_id[1:]
    print("Selected playlist:", playlist_id)
    go_obj.get_playlist(playlist_id)
    print("Created Honeycomb playlist")
    return jsonify(result="1")


@app.route('/playNew')
def web_play():
    print("Playing Honeycomb playlist")
    data = go_obj.play_new()
    return jsonify(result=data)


if __name__ == '__main__':
    # set environment variables
    # load json
    with open('spotify_keys.json') as f:
        data = json.load(f)
        os.environ["SPOTIPY_CLIENT_ID"] = data['client_id']
        os.environ["SPOTIPY_CLIENT_SECRET"] = data['client_secret']
        os.environ["SPOTIPY_REDIRECT_URI"] = data['redirect_uri']

    # serve with eventlet
    wsgi.server(listen(('', 5000)), app)
