import sqlite3                                                                  # importerar sqlite3
import os


class DB:                                                                       # skapar en DB klass
    db_url: str

    def __init__(self, db_url: str):
        self.db_url = db_url                                                    # skapar db url

        if not os.path.exists(self.db_url):                                     # om den inte finns skapas den
            self.init_db()

    def call_db(self, query, *args):     
        conn = sqlite3.connect(self.db_url)                                     # initierar databas
        cur = conn.cursor()
        res = cur.execute(query, args)
        data = res.fetchall()
        cur.close()
        conn.commit()
        conn.close()
        return data

    def init_db(self):
        init_db_query = """                                                      # skapar tabell
        CREATE TABLE IF NOT EXISTS song (
            id INTEGER PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            artist VARCHAR(255) NOT NULL
            genre VARCHAR(255) NOT NULL
        );
        """

        insert_query = """                                                      # lägger till data
        INSERT INTO song (title, artist, genre)
        VALUES ('A', 'B', 'C');
        """
        self.call_db(init_db_query)   
        self.call_db(insert_query)