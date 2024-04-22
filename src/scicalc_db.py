import sqlite3

class SciCalcDatabase:
    """
    This class represents a SQLite database for storing equations and results.
    Attributes:
    """
    def __init__(self, db_file='calculator.db'):
        self.db_file = db_file
        self.db = None

    def connect(self):
        try:
            self.db = sqlite3.connect(self.db_file)
        except sqlite3.Error:
            print("Error connecting to the database.")
        self._create_table()

    def _create_table(self):
        try:
            with self.db:
                self.db.execute('''
                    CREATE TABLE IF NOT EXISTS Equations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        equation TEXT,
                        result TEXT
                    )
                ''')
        except sqlite3.Error:
            print("Error creating the table.")

    def save_history(self, equation, result):
        try:
            with self.db:
                self.db.execute(
                    'INSERT INTO Equations (equation, result) VALUES (?, ?)', (equation, result)
                )
        except sqlite3.Error:
            print("Error saving equation to the database.")

    def load_history(self):
        try:
            with self.db:
                cursor = self.db.execute('SELECT equation, result FROM Equations ORDER BY id')
                return cursor.fetchall()
        except sqlite3.Error:
            print("Error loading equations from the database.")
            return []

    def clear_history(self):
        try:
            with self.db:
                self.db.execute('DELETE FROM Equations')
        except sqlite3.Error:
            print("Error clearing history in the database.")

    def close_connection(self):
        if self.db is not None:
            self.db.close()
            self.db = None
