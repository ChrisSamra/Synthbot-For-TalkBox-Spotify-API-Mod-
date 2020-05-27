# Synthbot-For-TalkBox-Spotify-API-Mod-
Takes Spotify pitch data from a selected song and turns the pitches into key presses that play the keys of the song on websynths.com

This is a modification of main.py from the spotify-api-starter-master found here: https://github.com/markkohdev/spotify-api-starter

In order to use this mod, setup the spotify-api-starter found from the link above (read it's readme and go through the steps) and change the code from main.py to this modified version.

Then in the terminal run the make file, make sure you've run the commands: 
export SPOTIPY_CLIENT_ID='your-spotify-client-id'
export SPOTIPY_CLIENT_SECRET='your-spotify-client-secret' 
export SPOTIPY_REDIRECT_URI='http://localhost/' 

After that, in a browser, open websynths.com beside the running program, go to tuning and set the number of keys to 12.
Also under tuning set "key" to "none" and then change the pitch system from "equal-tempered" to "manual".

Now in the terminal find the song of your choice and select "Audio Analysis (Low-Level)"
Right after selecting that, move your cursor to and select the browser window with websynths open and wait 5 seconds.

The modified script takes the relevant data from the low level audio analysis and uses that to determine what keys to press.

IMPORTANT NOTE: Sometimes depending on the song the software will play c# when it needs to play d, this due to the data not being perfect.
To solve this, on the website go to the frequency of the c# key and change it to the frequency of d, it's a band-aid fix I know but it works.
