import lyricsgenius
import json
import re
import pprint
import pymongo
from pymongo import MongoClient

def json_lyrics_creation(filename = "output_songs.json",
                         artist_name = "Steven Universe", 
                         max_songs = 3,
                         token = "znGu5Y5LvZ2pMT3XxHmU-jPMC3bTqpysfTiKOzew49nSiyqDbgSBnfNGUh1_AYRH",
                         mydb = MongoClient('localhost', 27017)["mydatabase"]):
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

    # Save it locally
    with open(filename, 'w') as json_file:
        json.dump(SUsongs, json_file)
    
    # Save it in the database
    mydb["steven_universe"].insert_one(SUsongs)
    
    

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

def retreive_data_mongo(mydb):
    pp = pprint.PrettyPrinter(width=200, indent=1)
    collection_song = mydb["steven_universe"]
    result = []

    for x in collection_song.find():
        result.append(x)
    
    return result


client = MongoClient('localhost', 27017)
mydb = client["mydatabase"]

json_lyrics_creation(mydb = mydb)
data_list = retreive_data_mongo(mydb)

#QUERIES

def q1(mydb): #list of songs
    cursor = mydb["steven_universe"].find({}) #song mist
    print("list of songs")
    for i in cursor:
        print (i['songs'][0]['title'])

def q2(mydb): #list of singer+
    singer_list = [] #singer/nbr song
    singer_nbr = []
    cursor = mydb["steven_universe"].find({}) #song mist
    for i in cursor:
        for j in (i['songs'][0]['lyrics']):
            if j['singer'] in singer_list:
                index = singer_list.index(j['singer'])
                singer_nbr[index] += 1
            else:
                singer_list.append(j['singer'])
                index = singer_list.index(j['singer'])
                singer_nbr.append(1)
    
    for i in range(len(singer_list)):
        print('singer:',singer_list[i], ' number of song:',singer_nbr[i])


q1(mydb)
q2(mydb)
    