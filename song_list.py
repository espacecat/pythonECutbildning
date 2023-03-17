
from dotenv import load_dotenv                                                  # kopplar ihop key-values från olika filer

load_dotenv()                                                                   # laddar environment variables från .env.

import os                                                                       # importerat os bibliotek
from typing import List
import requests                                                                 # pipenv install requests

from musical_shuffle_app import Song                                            # importerar klass "Song" från API-filen musical_shuffle_app



DB_URL = os.getenv("DB_URL")                                                    # definierar DB_URL


def url(route: str):                                                            
    return f"{DB_URL}{route}"                               


print("Hello, please choose one of the following options: ")

def print_menu():                                                                # meny med alternativ som printas
    print(                                                                       # överensstämmer med routerna
        """
    1: Add Song
    2: Add Artist
    3: Get song
    4: Get Artist
    5: Delete Song
    6: Update Song
    7: Exit program
    """
    )
    pass

def add_song():                                                                  #anropar funktion meny1
    print("Add song")
    title = input("Song Title: ")
    artist = input("Artist Name: ")
    genre = input("Genre: ")
    new_song = Song(title=title, artist=artist, genre=genre)                     # lägger till automatiskt i "Song" datanbasen.
    res = requests.post(url("/add_song"), json=new_song.dict())         
    print(res)
    pass

def add_artist():                                                                # anropar funktion meny2
    print("Add artist")
    title = input("Song Title: ")
    artist = input("Artist Name: ")
    genre = input("Genre: ")
    new_artist = Song(title=title, artist=artist, genre=genre)
    res = requests.post(url("/add_artist"), json=new_artist.dict())
    print(res)
    pass

def get_songs():                                                                  #anropar funktion meny3
    songs = []                                                                   # skapar en lista 
    print("Get song")
    res = requests.get(url("/allsongs"))
    if not res.status_code == 200:
        return
    data = res.json()
    for song in data:
        song = Song(**song)                                                      # fångar alla element i klass Song
        print("__________")
        print(f"ID: {song.id}")
        print(F"title: {song.title}")
        print(f"artist: {song.artist}")
        print(f"genre: {song.genre}")
        songs.append(song)                                                       # appendar listan
    return songs                                                                 # returnerar hela listan 

def get_artists():                                                                # anropar funktion meny4
    songs = []
    print("Get artist")
    res = requests.get(url("/allartists"))
    if not res.status_code == 200:
        return
    data = res.json()
    for song in data:
        song = Song(**song)
        print("__________")
        print(f"ID: {song.id}")
        print(F"title: {song.title}")
        print(f"artist: {song.artist}")
        print(f"genre: {song.genre}")
        songs.append(song)
    return songs

def delete_song():                                                              # anropar funktion meny5
    print("Delete song")
    song_to_delete = input("Please give the id of the song you'd like to delete: ")
    if not str.isdigit(song_to_delete):
        print("Ids are integers")
        return
    res = requests.delete(url(f"/delete_song/{song_to_delete}"))
    print(res.json())
    

def update_song(songs: List[Song]):                                             # anropar funktion meny6
    print("Update song", songs)
    song_to_update = input("Id of song you wish to update: ")
    if not str.isdigit(song_to_update):                                         # måste vara int
        print("Ids are integers")
        return
    
    index = None                                
    for i, song in enumerate(songs):                                            # om index finns i listan
        print(song.id)
        if song.id == int(song_to_update):                                      # välj för att uppdatera
            index = i
            break
    

    if index == None:                                                           # om id inte finns eller är str
        print("No such song")
        return                                                                  # avslutas update funktionen
    song = songs[index]

    title = input("Song title (leave blank if same): ")
    artist = input("Artist name (leave blank if same): ")
    genre = input("Genre (leave blank if same):")

    if not title:                                                              # behåller original låten
        title = song.title
    if not artist:                                                             # behåller original artisten
        artist = song.artist
    if not genre:                                                              # behåller original genten
        genre = song.genre

    new_song = Song(title=title, artist=artist, genre=genre)                   # skapar en ny låt
    res = requests.put(url(f"/update_song/{song_to_update}"), json=new_song.dict())
    print(res.json())

    

def main():
    print_menu()
    options = input("Please choose the action you'd like to take: ")           # ber om input från användare
    options = options.strip()                                                  # tar bort onödiga mellanslag
    if not str.isdigit(options):                                               # ber om int, vid str input ber den om ny input
        print("Please enter an available option")
        return
    
    match int(options):                                                        # definierade menyalternativen, använder match istället för if else 
        case 1:                                                                # alternativ för att lägga till låt/artist
            add_song()
        case 2:                                                                # alternativ för att lägga till artist/låt
            add_artist()
        case 3:                                                                # alternativ för att hämta låt/artist
            songs = get_songs()
        case 4:                                                                # alternativ för att hämta artist/låt
            songs = get_artists()
        case 5:                                                                # raderar specifik låt
            delete_song()
        case 6:                                                                # uppdaterar specifik låt
            songs = get_songs()
            update_song(songs)
        case 7:                                                                # avslutar programmet                            
            exit()
        case _:
            print("Please enter an available option")

              
    

while __name__ == "__main__":                                                  # så länge name (filen som körs)= main 
    main()                                                                     # fortsätter den att ge meny alternativ 
