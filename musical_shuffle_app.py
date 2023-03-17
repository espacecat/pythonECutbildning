
from typing import List
from fastapi import FastAPI                                                 # importerar API:et
from pydantic import BaseModel                                              # importerar basemodel för att skapa klass

from db import DB                                                           # från db filen importeras DB klass

class Song(BaseModel):                                                      # definierar klass Song
    id: int = None              
    title: str
    artist: str
    genre: str



app = FastAPI()                                                             # definierar API objekt
db = DB("songs.db")                                                         # kopplar databasen

curr_id = 1
app.songs: List[Song] = []                                                  # skapar en lista "songs"

@app.get("/")                                                               # "get" route nr1
def root():
    return "Hello and welcome to Nadjas Musical Shuffle!"

@app.get("/allsongs")                                                       # "get" route nr2
def get_songs():                                                            
    get_song_query = """                                                    # query till sql 
    SELECT * FROM song
    """
    data = db.call_db(get_song_query)                                       # query definierad 
    songs = []
    for element in data:
        id, title, artist, genre = element
        songs.append(Song(id=id, title=title, artist=artist, genre=genre))
        print(data)
    return songs

@app.get("/allartists")                                                     # "get" route nr3
def get_artists():
    get_artist_query = """                                                  # fetchar alla låtar från db
    SELECT * FROM song
    """
    data = db.call_db(get_artist_query)
    songs = []                                                              # anropar lista songs
    for element in data:
        id, title, artist, genre = element
        songs.append(Song(id=id, title=title, artist=artist, genre=genre))
        print(data)
    return songs

@app.get("/song/{id}")                                                      # "get" route nr 4
def get_song(id: int):
    return "Returns a song with specific id " + str(id)

@app.post("/add_song")                                                      # "post" route nr 1
def add_song(song: Song):
    insert_query = """
    INSERT INTO song (title, artist, genre)
    VALUES ( ?, ?)
    """
    db.call_db(insert_query, song.title, song.artist, song.genre)           # lägger till i sql-tabellen
    return "Adds a song"

@app.post("/add_artist")                                                    # "post" route nr 2
def add_artist(song: Song):
    insert_query = """
    INSERT INTO song (artist, title, genre)
    VALUES ( ?, ?)
    """
    db.call_db(insert_query, song.artist, song.title, song.genre)           # lägger till i tabellen 
    return "Adds an artist"

@app.delete("/delete_song/{id}")                                            # "delete" route nr 1
def delete_song(id: int):
    delete_query = """                                                      # raderar låt från db
    DELETE FROM song WHERE id = ?
    """
    db.call_db(delete_query, id)                                            
    return True

@app.put("/update_song/{id}")                                              # update route nr 1
def update_song(id: int, new_song: Song):                                  # uppdaterar och lägger till ny låt i listan
    update_song_query = """                                                # uppdaterar och lägger till i tabellen
    UPDATE song
    SET title = ?, artist = ?, genre = ?
    WHERE id = ?
    """
    db.call_db(update_song_query, new_song.title, new_song.artist, new_song.genre, id)          # uppdaterar tabellen
    return True
