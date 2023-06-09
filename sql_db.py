import pyodbc

db_server = "DESKTOP-1CQF68U\SQLEXPRESS"                                        # laptop server
db_name = "songs"                                                               # databas namn
db_driver = "ODBC Driver 17 for SQL Server"                                     # fungerande driver vald

connection_string = f"""
DRIVER={db_driver};
SERVER={db_server};
DATABASE={db_name};
trusted_connection=yes;
"""


class DB:
    def call_db(self, query, *args):
        data = None
        conn = pyodbc.connect(connection_string)
        cur = conn.cursor()
        if "SELECT" in query:
            res = cur.execute(query, args)
            data = res.fetchall()
            cur.commit()
            cur.close()
        else:
            conn.execute(query, args)
        conn.commit()
        conn.close()
        return data

    def init_db(self):
        init_db_query = """
        DROP TABLE song;
        CREATE TABLE song (
            id INTEGER PRIMARY KEY IDENTITY(1,1) NOT NULL,
            title VARCHAR(255) NOT NULL,
            artist VARCHAR(255) NOT NULL,
            genre VARCHAR(255) NOT NULL
        );
        """
        insert_query = """
        INSERT INTO song (title, artist, genre)
        VALUES ('A', 'B', 'C');
        """
        conn = pyodbc.connect(connection_string)
        conn.execute(init_db_query)
        conn.execute(insert_query)
        conn.commit()
        conn.close()


if __name__ == "__main__":
    db = DB()

    db.init_db()