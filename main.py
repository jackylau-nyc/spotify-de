import pandas as pd
import requests
import json
import datetime

# Python files for ETL process
from extract import get_spotify_data
from transform import check_if_valid_data
from load import load_spotify_data

if __name__ == "__main__":

    # EXTRACT
    songs_df = get_spotify_data()
    print(songs_df)
    
    # VALIDATE
    if check_if_valid_data(songs_df):
        print("\nValid data received\n")
    
    # LOAD
    load_spotify_data(songs_df)