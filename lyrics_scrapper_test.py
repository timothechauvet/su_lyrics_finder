import lyricsgenius
import json
import pandas as pd
import numpy as np
import string
import re

def csv_lyrics_creation(filename = "output_songs.csv",
                         artist_name = "Steven Universe", 
                         max_songs = 15,
                         token = "dyuHwfM-LUID2D_Ia9vEZneBJLidAlHgasnNyzdBdYkQb7Qrx37E0aIVB51qNuSw"):
    # Connect to Genius API                         
    genius = lyricsgenius.Genius(token)

    genius.verbose = False # Turn off status messages
    genius.remove_section_headers = True # Remove section headers (e.g. [Chorus]) from lyrics when searching
    genius.skip_non_songs = True # Include hits thought to be non-songs (e.g. track lists)
    #genius.excluded_terms = [] # Exclude songs with these words in their title

    # Fetch all songs by artist "Steven Universe"
    SUsongs = {}
    SUsongs["songs"] = []
    SUsongs["lyrics"] = []

    artist = genius.search_artist(artist_name=artist_name, max_songs=max_songs, sort="title")
    for song in artist.songs:
        song_lyrics = re.sub("\n", " ", song.lyrics)
        song_name = song.title
        
        # Remove null songs and append them to the JSON
        if (song_lyrics != "") and (song_name != ""):
            # tmp = {}
            # tmp["name"] = []
            # tmp["lyrics"]
            SUsongs["songs"].append(song_name)
            SUsongs["lyrics"].append(song_lyrics)
    
    df = pd.DataFrame(SUsongs)
    df.to_json(path_or_buf = "output_songs.json")

def clean_data(filename = "output_songs.csv"):
    # Open the filename
    with open(filename, "r") as read_file:
        df = pd.read_csv(filename)

    del df['Unnamed: 0']
    print(list(df.columns))
    print(df)
    return df

csv_lyrics_creation()
#df = clean_data()