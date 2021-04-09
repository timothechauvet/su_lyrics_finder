import lyricsgenius
import json
import pandas as pd
import numpy as np
import string
import re
import pprint

def json_lyrics_creation(filename = "output_songs.json",
                         artist_name = "Steven Universe", 
                         max_songs = 15,
                         token = "znGu5Y5LvZ2pMT3XxHmU-jPMC3bTqpysfTiKOzew49nSiyqDbgSBnfNGUh1_AYRH"):
    pp = pprint.PrettyPrinter(width=200, indent=1)
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
        song_name = song.title

        song_lyrics = clean_lyrics(song.lyrics)
        
        # Remove null songs, songs with no singers written and unnamed songs
        if(len(song_lyrics) > 0 and (song_name != "")):
            if(len(song_lyrics[0]["singer"]) > 0):
                song = {}
                song["title"] = song_name
                song["lyrics"] = song_lyrics
                SUsongs["songs"].append(song)
    
    with open(filename, 'w') as json_file:
        json.dump(SUsongs, json_file)

def clean_lyrics(raw_song):
    # Main regex for dispatching singers and lyrics
    regex_singer = r"\S+(?:(?=:))"
    regex_lyrics = r"(?:(?<=:\s))(.+?)(?:(?= \S+:)|(?=$)|(?=\n))"

    # Regex for cleaning annotations and double spaces
    regex_parenthesis   = r"(\(.*?\))"
    regex_double_space  = r"(\s{2,})"

    # Remove unwanted data
    raw_song = re.sub("\n", " ", raw_song)
    raw_song = re.sub(regex_parenthesis, '', raw_song)
    raw_song = re.sub(regex_double_space, ' ', raw_song)

    # Add the singer & lyrics
    result_singer   = re.findall(regex_singer, raw_song, re.S)
    result_line     = re.findall(regex_lyrics, raw_song, re.S)

    # Uppercase singers and lowercase lyrics for better processing
    result_singer   = [x.upper() for x in result_singer]
    result_line     = [x.lower() for x in result_line]

    # Dispatch all lyrics for better Json readability
    lyrics = []
    for i in range(len(result_singer)):
        curr_line = {}
        curr_line["line"]    = result_line[i]
        curr_line["singer"]  = result_singer[i]
        lyrics.append(curr_line)
    
    return lyrics

json_lyrics_creation()