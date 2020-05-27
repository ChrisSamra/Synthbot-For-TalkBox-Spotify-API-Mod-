import sys
import requests
import os
import json
import math
import spotipy
import spotipy.util as sp_util
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOauthError
from spotipy.client import SpotifyException
from pynput.keyboard import Key, Controller
import time


from display_utils import (
    print_header,
    track_string,
    print_audio_features_for_track,
    print_audio_analysis_for_track,
    choose_tracks
    )

from common import (
    authenticate_client,
    authenticate_user,
    fetch_artists,
    fetch_artist_top_tracks
    )

# Define the scopes that we need access to
# https://developer.spotify.com/web-api/using-scopes/
scope = 'user-library-read playlist-read-private'


################################################################################
# Main Demo Function
################################################################################

def main():
    """
    Our main function that will get run when the program executes
    """
    print_header('Spotify Web API Demo App', length=50)

    # Run our demo function
    retry = True
    while retry:
        try:
            print("""
Let's get some audio data!  How would you like to choose your tracks:
  1.) Search for a song
  2.) Choose from your playlists
  3.) Pick from your saved songs""")
            program_choice = input('Choice: ')
        except ValueError as e:
            print('Error: Invalid input.')

        spotify = None
        selected_tracks = []
        if program_choice == '1':
            spotify = authenticate_client()
            selected_tracks = search_track(spotify)
        elif program_choice == '2':
            username, spotify = authenticate_user()
            selected_tracks = list_playlists(spotify, username)
        elif program_choice == '3':
            username, spotify = authenticate_user()
            selected_tracks = list_library(spotify, username)

        if selected_tracks:
            try:
                print("""
Great, we have {} {}!  What would you like to see for these tracks:
    1.) Audio Features (High-Level)
    2.) Audio Analysis (Low-Level)""".format(len(selected_tracks),
        ("tracks" if len(selected_tracks) > 1 else "track")))
                display_choice = input('Choice: ')
            except ValueError as e:
                print('Error: Invalid input.')

            if display_choice == '1':
                get_audio_features(spotify, selected_tracks, pretty_print=True)
            elif display_choice == '2':
                get_audio_analysis(spotify, selected_tracks, pretty_print=True)


        # Prompt the user to run again
        retry_input = input('\nRun the program again? (Y/N): ')
        retry = retry_input.lower() == 'y'


################################################################################
# API Fetch Functions
################################################################################

def get_audio_features(spotify, tracks, pretty_print=False):
    """
    Given a list of tracks, get and print the audio features for those tracks!
    :param spotify: An authenticated Spotipy instance
    :param tracks: A list of track dictionaries
    """
    if not tracks:
        print('No tracks provided.')
        return

    # Build a map of id->track so we can get the full track info later
    track_map = {track.get('id'): track for track in tracks}

    # Request the audio features for the chosen tracks (limited to 50)
    print_header('Getting Audio Features...')
    tracks_features_response = spotify.audio_features(tracks=track_map.keys())
    track_features_map = {f.get('id'): f for f in tracks_features_response}

    # Iterate through the features and print the track and info
    if pretty_print:
        for track_id, track_features in track_features_map.items():
            # Print out the track info and audio features
            track = track_map.get(track_id)
            print_audio_features_for_track(track, track_features)

    return track_features_map





# synthbot function determines what keys to press on virtual keyboard based on pitch data 
# websynths.com is what I used, the analysis data only supports an octave (black and white keys) so on the website set the key count to 12

def synthbot(data):

    keyboard = Controller()

    if isinstance(data["note_value"], list): #case 1: multiple notes at a given time
        
        note_ref = {"z": 0 , "x": 1, "c": 2, "v": 3, "b": 4, "n":5, "m":6, ",":7, ".":8, "/":9, "a":10, "s":11}

        for note in data["note_value"]:
            if note == note_ref["z"]:
                keyboard.press('z')

            elif note == note_ref["x"]:
                keyboard.press('x')

            elif note == note_ref["c"]:
                keyboard.press('c')

            elif note == note_ref["v"]:
                keyboard.press('v')

            elif note == note_ref["b"]:
                keyboard.press('b')

            elif note == note_ref["n"]:
                keyboard.press('n')

            elif note == note_ref["m"]:
                keyboard.press('m')

            elif note == note_ref[","]:
                keyboard.press(',')

            elif note == note_ref["."]:
                keyboard.press('.')

            elif note == note_ref["/"]:
                keyboard.press('/')

            elif note == note_ref["a"]:
                keyboard.press('a')

            elif note == note_ref["s"]:
                keyboard.press('s')

        time.sleep(data["note_duration"]-0.005) #controls duration of key press
        keyboard.release('z')
        keyboard.release('x')
        keyboard.release('c')
        keyboard.release('v')
        keyboard.release('b')
        keyboard.release('n')
        keyboard.release('m')
        keyboard.release(',')
        keyboard.release('.')
        keyboard.release('/')
        keyboard.release('a')
        keyboard.release('s')
                
    else: #case 2: only one prominent note
        if data["note_value"] == 0:
            keyboard.press('z')
            time.sleep(data["note_duration"]-0.01)
            keyboard.release('z')

        elif data["note_value"] == 1:
            keyboard.press('x')
            time.sleep(data["note_duration"]-0.01)
            keyboard.release('x')

        elif data["note_value"] == 2:
            keyboard.press('c')
            time.sleep(data["note_duration"]-0.01)
            keyboard.release('c')

        elif data["note_value"] == 3:
            keyboard.press('v')
            time.sleep(data["note_duration"]-0.01)
            keyboard.release('v')

        elif data["note_value"] == 4:
            keyboard.press('b')
            time.sleep(data["note_duration"]-0.01)
            keyboard.release('b')

        elif data["note_value"] == 5:
            keyboard.press('n')
            time.sleep(data["note_duration"]-0.01)
            keyboard.release('n')

        elif data["note_value"] == 6:
            keyboard.press('m')
            time.sleep(data["note_duration"]-0.01)
            keyboard.release('m')

        elif data["note_value"] == 7:
            keyboard.press(',')
            time.sleep(data["note_duration"]-0.01)
            keyboard.release(',')

        elif data["note_value"] == 8:
            keyboard.press('.')
            time.sleep(data["note_duration"]-0.01)
            keyboard.release('.')

        elif data["note_value"] == 9:
            keyboard.press('/')
            time.sleep(data["note_duration"]-0.01)
            keyboard.release('/')

        elif data["note_value"] == 10:
            keyboard.press('a')
            time.sleep(data["note_duration"]-0.01)
            keyboard.release('a')

        elif data["note_value"] == 11:
            keyboard.press('s')
            time.sleep(data["note_duration"]-0.01)
            keyboard.release('s')
        else:
            print("no notes cheif")





#get_audio_analysis is modified to take relevant analysis data and send it to the synthbot function

def get_audio_analysis(spotify, tracks, pretty_print=False):
    """
    Given a list of tracks, get and print the audio analysis for those tracks!
    :param spotify: An authenticated Spotipy instance
    :param tracks: A list of track dictionaries
    """
    if not tracks:
        print('No tracks provided.')
        return

    # Build a map of id->track so we can get the full track info later
    track_map = {track.get('id'): track for track in tracks}

    # Request the audio analysis for each track -- one at a time since these
    # can be really big
    tracks_analysis = {}

    #i = 0
    print_header('Getting Audio Audio Analysis...')
    for track_id in track_map.keys():
        analysis = spotify.audio_analysis(track_id)
        tracks_analysis[track_id] = analysis
        
        # Print out the track info and audio features
        if pretty_print:
            track = track_map.get(track_id)


            #not necessary, just sets up txt file to print song data to, this was for testing purposes
            new_path = '/Users/chrissamra/Desktop/spotify-api-starter-master/src/song.txt'
            new_song = open(new_path,'w+')
            new_song.write('\n''{}'.format(track_string(track)+'\n'))
            new_song.write('{ "notes" : [\n')

            print('{}'.format(track_string(track))) #returns track name 

            time.sleep(5) #waits 5 seconds before starting

            i=0
            for seg in analysis["segments"]: #iterates through every segment of the song

                pitches = []
                
                for cur_pitch in seg.get("pitches"): #checks every pitch in current segment
                    
                    #if pitch confidence is over 75% add to list of pitches
                    if cur_pitch >= 0.75:
                        pitches.append(cur_pitch)


                #if multiple pitches are over 75% confidence
                if len(pitches) > 1:
                    cleanDict = {"note_time" : seg.get("start"), "note_duration" : seg.get("duration"), "note_value" : pitches } #gets relevant segment info 
                    synthbot(cleanDict) #sends data to synthbot function

                # if the first pitch and consecutive pitches in the list are normalized to 1 (no noize)
                elif seg.get("pitches").index(1.0) == 0 and seg.get("pitches")[1] == 1 : 
                    pitch = -1
                    cleanDict = {"note_time" : seg.get("start"), "note_duration" : seg.get("duration"), "note_value" : pitch } #gets relevant segment info
                    synthbot(cleanDict) #sends data to synthbot function

                #if only one pitch has over 75% confidence
                else:
                    pitch = seg.get("pitches").index(1.0)
                    cleanDict = {"note_time" : seg.get("start"), "note_duration" : seg.get("duration"), "note_value" : pitch } #gets relevant segment info
                    synthbot(cleanDict) #sends data to synthbot function
                
                #not necessary, just outputs song data to terminal for testing purposes
                new_song.write(json.dumps(cleanDict, indent=2)+',')
                print(json.dumps(cleanDict, indent=2)) 

                i += 1

            #not necessary, just outputs song data to txt file for testing purposes
            new_song=open(new_path,"r")
            d=new_song.read()
     
            m=d.split("\n")
            s="\n".join(m[:-1])
            new_song.close()
            new_song=open(new_path,"w+")
            for n in range(len(s)):
                new_song.write(s[n])
                        
            new_song.write('}]}')
            print("total segments:"+ str(i)+"")
            new_song.close()

    return tracks_analysis




################################################################################
# Demo Functions
################################################################################

def search_track(spotify):
    """
    This demo function will allow the user to search a song title and pick the song from a list in order to fetch
    the audio features/analysis of it
    :param spotify: An basic-authenticated spotipy client
    """
    keep_searching = True
    selected_track = None

    # Initialize Spotipy
    spotify = authenticate_client()

    # We want to make sure the search is correct
    while keep_searching:
        search_term = input('\nWhat song would you like to search: ')

        # Search spotify
        results = spotify.search(search_term)
        tracks = results.get('tracks', {}).get('items', [])

        if len(tracks) == 0:
            print_header('No results found for "{}"'.format(search_term))
        else:
            # Print the tracks
            print_header('Search results for "{}"'.format(search_term))
            for i, track in enumerate(tracks):
                print('  {}) {}'.format(i + 1, track_string(track)))

        # Prompt the user for a track number, "s", or "c"
        track_choice = input('\nChoose a track #, "s" to search again, or "c" to cancel: ')
        try:
            # Convert the input into an int and set the selected track
            track_index = int(track_choice) - 1
            selected_track = tracks[track_index]
            keep_searching = False
        except (ValueError, IndexError):
            # We didn't get a number.  If the user didn't say 'retry', then exit.
            if track_choice != 's':
                # Either invalid input or cancel
                if track_choice != 'c':
                    print('Error: Invalid input.')
                keep_searching = False

    # Quit if we don't have a selected track
    if selected_track is None:
        return

    # Request the features for this track from the spotify API
    # get_audio_features(spotify, [selected_track])

    return [selected_track]



def list_playlists(spotify, username):
    """
    Get all of a user's playlists and have them select tracks from a playlist
    """
    # Get all the playlists for this user
    playlists = []
    total = 1
    # The API paginates the results, so we need to iterate
    while len(playlists) < total:
        playlists_response = spotify.user_playlists(username, offset=len(playlists))
        playlists.extend(playlists_response.get('items', []))
        total = playlists_response.get('total')

    # Remove any playlists that we don't own
    playlists = [playlist for playlist in playlists if playlist.get('owner', {}).get('id') == username]

    # List out all of the playlists
    print_header('Your Playlists')
    for i, playlist in enumerate(playlists):
        print('  {}) {} - {}'.format(i + 1, playlist.get('name'), playlist.get('uri')))

    # Choose a playlist
    playlist_choice = int(input('\nChoose a playlist: '))
    playlist = playlists[playlist_choice - 1]
    playlist_owner = playlist.get('owner', {}).get('id')

    # Get the playlist tracks
    tracks = []
    total = 1
    # The API paginates the results, so we need to keep fetching until we have all of the items
    while len(tracks) < total:
        tracks_response = spotify.user_playlist_tracks(playlist_owner, playlist.get('id'), offset=len(tracks))
        tracks.extend(tracks_response.get('items', []))
        total = tracks_response.get('total')

    # Pull out the actual track objects since they're nested weird
    tracks = [track.get('track') for track in tracks]

    # Print out our tracks along with the list of artists for each
    print_header('Tracks in "{}"'.format(playlist.get('name')))

    # Let em choose the tracks
    selected_tracks = choose_tracks(tracks)

    return selected_tracks


def list_library(spotify, username):
    """
    Get all songs from tthe user's library and select from there
    """

    # Get all the playlists for this user
    tracks = []
    total = 1
    first_fetch = True
    # The API paginates the results, so we need to iterate
    while len(tracks) < total:
        tracks_response = spotify.current_user_saved_tracks(offset=len(tracks))
        tracks.extend(tracks_response.get('items', []))
        total = tracks_response.get('total')

        # Some users have a LOT of tracks.  Warn them that this might take a second
        if first_fetch and total > 150:
            print('\nYou have a lot of tracks saved - {} to be exact!\nGive us a second while we fetch them...'.format(
                total))
            first_fetch = False

    # Pull out the actual track objects since they're nested weird
    tracks = [track.get('track') for track in tracks]

    # Let em choose the tracks
    selected_tracks = choose_tracks(tracks)

    # # Print the audio features :)
    # get_audio_features(spotify, selected_tracks)

    return selected_tracks

if __name__ == '__main__':
    main()
