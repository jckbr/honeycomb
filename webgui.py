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
    go_obj.connect()
    return jsonify(result="1")


@app.route('/loadPlaylists')
def web_load_playlists():
    playlist_data = go_obj.load_playlists()
    return jsonify(result=playlist_data)


@app.route('/select')
def web_select():
    playlist_id = request.args.get('plID', 0)
    playlist_id = playlist_id[1:]
    go_obj.get_playlist(playlist_id)
    return jsonify(result="1")


@app.route('/playNew')
def web_play():
    playlist_data = go_obj.play_new()
    return jsonify(result=playlist_data)


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
