import sqlite3 as sql
db_file = 'delivery.db'

def create_schema():
    with sql.connect(db_file) as con:
        cur = con.cursor()
        try:
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute( """
                        CREATE TABLE users(user_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, lastname1 TEXT NOT NULL, 
                        lastname2 TEXT NOT NULL, email TEXT NOT NULL UNIQUE, username TEXT NOT NULL UNIQUE, password TEXT NOT NULL)
                        """)
            cur.execute("""
                            CREATE TABLE packages(package_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, lat INTEGER, lon INTEGER,
                            price FLOAT, user_id TEXT NOT NULL, FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE )
                        """)
            con.commit()
            con.close()
        except sql.OperationalError:
            pass

def get_db_connection():
    with sql.connect(db_file) as con:
        cur = con.cursor()
        cur.execute("PRAGMA foreign_keys = ON")
    return con
    