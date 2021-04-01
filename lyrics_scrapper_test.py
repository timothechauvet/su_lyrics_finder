import lyricsgenius, json, pandas as pd, numpy as np, string

def csv_lyrics_creation(filename = "output_songs.csv",
                         artist_name = "Steven Universe", 
                         max_songs = 5,
                         token = "ACB6RV-hkWn5XMSBGZW0tSClcrztg-Zkql2p_qVhs799QFsHWgQ6_Gnpe430M-Bv"):
    # Connect to Genius API                         
    genius = lyricsgenius.Genius(token)

    genius.verbose = False # Turn off status messages
    genius.remove_section_headers = True # Remove section headers (e.g. [Chorus]) from lyrics when searching
    genius.skip_non_songs = True # Include hits thought to be non-songs (e.g. track lists)
    #genius.excluded_terms = [] # Exclude songs with these words in their title

    # Fetch all songs by artist "Steven Universe"
    artist = genius.search_artist(artist_name=artist_name, max_songs=max_songs, sort="title")

    SUsongs = {}
    SUsongs["titles"] = []
    SUsongs["lyrics"] = []
    for song in artist.songs:
        if(song.lyrics != ""):
            SUsongs["titles"].append(song.title)
            SUsongs["lyrics"].append(song.lyrics)

    df = pd.DataFrame(SUsongs)
    
    # Save locally the DataFrame
    df.to_csv(filename)

def clean_data(filename = "output_songs.csv"):
    # Open the filename
    with open(filename, "r") as read_file:
        df = pd.read_csv(filename)

    del df['Unnamed: 0']
    print(list(df.columns))
    print(df)
    return df

csv_lyrics_creation()
df = clean_data()