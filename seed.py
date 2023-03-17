import json
from db import DB

db = DB("songs.db")

create_song = """
INSERT INTO song (
title, 
artist,
genre
) VALUES (
?, ?
)
"""


with open("seed.json", "r") as seed:
    data = json.load(seed)

    for song in data["song"]:
        db.call_db(create_song, song["title"], song["artist"], song["genre"])

