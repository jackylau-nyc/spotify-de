import datetime
import pandas as pd
from secrets import CLIENT_ID, CLIENT_SECRET
import requests
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth

def get_spotify_data():
    # Request headers
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                                                    redirect_uri="http://localhost/callback", scope="user-read-recently-played"))

    # Variables to be used for request
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000

    # Stores response as json object
    data = sp.current_user_recently_played(after=yesterday_unix_timestamp)
    print(data)
    # Lists to store extracted data
    song_names = []
    artist_names = []
    played_at = []
    timestamps = []

    # Extracting only relevant data from json response 
    for song in data["items"]:
        song_names.append(song["track"]["name"])
        artist_names.append(song["track"]["album"]["artists"][0]["name"])
        played_at.append(song["played_at"])
        timestamps.append(song["played_at"][0:10])
    
    # Create dictionary from lists to turn into pandas dataframe
    song_dict = {
        "song_name": song_names,
        "artist_name": artist_names,
        "played_at": played_at,
        "timestamp": timestamps
    }
    
    # Pandas dataframe creation
    song_df = pd.DataFrame(song_dict, columns = ["song_name", "artist_name", "played_at", "timestamp"])
    return song_df