import lyricsgenius
import json
import pandas as pd
import numpy as np
import string
import re

def json_lyrics_creation(filename = "output_songs.json",
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

def clean_data(raw_song):
    # Main regex for dispatching singers and lyrics
    regex_singer = r"\S+(?:(?=:))"
    regex_lyrics = r"(?:(?<=:\s))(.+?)(?:(?= \S+:)|(?=$)|(?=\n))"

    # Regex for cleaning annotations and double spaces
    regex_parenthesis   = r"(\(.*?\))"
    regex_double_space  = r"(\s{2,})"

    # Remove unwanted data
    raw_song = re.sub(regex_parenthesis, '', raw_song)
    raw_song = re.sub(regex_double_space, ' ', raw_song)

    # Add the singer & lyrics
    result_singer   = re.findall(regex_singer, raw_song, re.S)
    result_line     = re.findall(regex_lyrics, raw_song, re.S)

    # Uppercase singers and lowercase lyrics for better processing
    for singer in result_singer:
        singer = singer.upper()
    for line in result_line:
        line = line.lower()

    # Dispatch all lyrics for better Json readability
    lyrics = {}
    for i in range(size(result_singer)):
        line = {}
        line["singer"]  = result_singer[i]
        line["line"]    = result_line[i]
        lyrics.append(line)
    
    return lyrics

csv_lyrics_creation()
#df = clean_data()