# honeycomb
This is a little passion project created while I was studying abroad in Germany during Spring 2022.

After authenticating through Spotify, a user can navigate pages of their playlists and select one they would like to copy the most recent 25 songs from. After selecting, the Python script creates/updates the Honeycomb playlist, removing old songs if needed, and adds the songs from the selected playlist. The user can then hit a **Play** button to immediately play the new playlist. If there are no active devices present, an alert is shown.

I created this project because I have a very large Spotify playlist (5,681 songs as of 05-13-2022) and I want to download recent songs in that playlsit to my phone for on-the-go. Instead of creating/updating a playlist with the new songs, I created this script and frontend page to do it for me.

This project use Bootstrap, HTML, CSS, Javascript, Flask, Python, and the [spotipy](https://spotipy.readthedocs.io/en/2.19.0/) Python package.

***

This was my first project that had a frontend attached to a backend Python script. A friend of mine helped get me started by attaching a frontend to my basic Python script using Flask and with other little things along the way.

In the future, I would like to rewrite this project as a full-stack project in Angular and make it more usable to others. It works but is not perfect yet.

I am also planning to put together a demo video to display the project until I rewrite the project as full-stack and host it personally.

Feel free to submit any issues found or suggestions! I am always looking to improve projects

<hr>

Spotify before creating new playlist:
<img src="Images/Screen Shot 2022-05-13 at 11.07.30 PM.png" width="25%">

Landing page:
<img src="Images/Screen Shot 2022-05-13 at 11.07.36 PM.png" width="25%">

After authenticating:
<img src="Images/Screen Shot 2022-05-13 at 11.07.42 PM.png" width="25%">

Playlist information when hovering:
<img src="Images/Screen Shot 2022-05-13 at 11.07.49 PM.png" width="25%">

Selected a playlist:
<img src="Images/Screen Shot 2022-05-13 at 11.07.58 PM.png" width="25%">

Spotify after creating new playlist:
<img src="Images/Screen Shot 2022-05-13 at 11.08.20 PM.png" width="25%">

After selecting **Play** to play new playlist on active device:
<img src="Images/Screen Shot 2022-05-13 at 11.08.25 PM.png" width="25%">

Error when no device is active:
<img src="Images/Screen Shot 2022-05-13 at 11.08.46 PM.png" width="25%">

***

Skills used/learned while creating Honeycomb:
- Bootstrap
- HTML
- CSS
- Javascript
- Flask
- Python
- [spotipy](https://spotipy.readthedocs.io/en/2.19.0/)
- [Spotify Web API](https://developer.spotify.com/documentation/web-api/quick-start/)
- Web application flow

***

**Disclaimer**:<br>
No license is associated with this project by design as this project is to be used for display and education of how the code works only.