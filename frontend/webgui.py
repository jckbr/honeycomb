from flask import Flask, render_template, request, jsonify
import os
import socket
import goPlaylist

#Setup custom flask HTML directoy
template_dir = os.path.dirname(__file__)
app = Flask(__name__, template_folder=template_dir, static_folder='./css')

#Serve index.html
@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')

#If a button is pressed, serve the color
@app.route('/connect')
def func1():
    print("Connected")
    goPlaylist.connect()
    return jsonify(result="1")
@app.route('/loadPlaylists')
def func2():
    print("Got playlists")
    data = goPlaylist.loadPlaylists()
    return jsonify(result=data)
@app.route('/select')
def func3():
    id = request.args.get('plID', 0)
    id = id[1:]
    print("Selected playlist:", id)
    goPlaylist.getPlaylist(id)
    print("Created Honeycomb playlist")
    return jsonify(result="1")
@app.route('/playNew')
def func4():
    print("Playing Honeycomb playlist")
    data = goPlaylist.playNew()
    return jsonify(result=data)

#Run the server on the local_ip and port 80
if __name__ == "__main__":
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    app.run(host=local_ip, port=5001, debug=False)