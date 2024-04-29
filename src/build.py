import sqlite3
from config import DATABASE_FILE_PATH

def build():
    """
    Builds the SQLite database by connecting, dropping existing tables and creating new tables.
    """
    connection = sqlite3.connect(DATABASE_FILE_PATH)
    drop_tables(connection)
    create_tables(connection)

def drop_tables(connection):
    """Drops the 'Equations' table if it exists.
    Args:
        connection (sqlite3.Connection): The connection to the SQLite database.
    """
    cursor = connection.cursor()
    cursor.execute("""DROP TABLE IF EXISTS Equations;""")
    connection.commit()

def create_tables(connection):
    """Creates the 'Equations' table.
    Args:
        connection (sqlite3.Connection): The connection to the SQLite database.
    """
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE Equations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            equation TEXT,
            result TEXT
        );
    """)
    connection.commit()
    print("Database created.")

if __name__ == "__main__":
    build()
