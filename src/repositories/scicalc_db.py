import sqlite3
from config import DATABASE_FILE_PATH

class SciCalcDatabase:
    """
    This class represents a SQLite database for storing equations and results.

    Attributes:
        db_file (str): The name of the SQLite database file.
        db (sqlite3.Connection): The connection to the SQLite database.
    """
    def __init__(self, view, db_file=DATABASE_FILE_PATH):
        """Initialize the SciCalcDatabase.

        Args:
            db_file (str): The name of the SQLite database file.
        """
        self.db_file = db_file
        self.db = None
        self.view = view

    def connect(self):
        """Establish a connection to the SQLite database."""
        try:
            self.db = sqlite3.connect(self.db_file)
            self.create_table()
        except sqlite3.Error:
            message = "Error connecting to the database."
            print(message)
            self.view.show_message(message)

    def create_table(self):
        """Create the 'Equations' table if it doesn't exist."""
        try:
            with self.db:
                self.db.execute('''
                    CREATE TABLE IF NOT EXISTS Equations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        equation TEXT,
                        result TEXT
                    )
                ''')
        except sqlite3.Error:
            message = "Error creating the table."
            print(message)
            self.view.show_message(message)

    def save_history(self, name, equation, result):
        """
        Save an equation and result to the 'Equations' table.
        Args:
            name (str): The name associated with the history entry.
            equation (str): The equation to be saved.
            result (str): The result to be saved.
        """
        try:
            with self.db:
                self.db.execute(
                    'INSERT INTO Equations (name, equation, result) VALUES (?, ?, ?)',
                    (name, equation, result)
                )
                self.db.commit()
        except sqlite3.Error:
            self.view.show_message("Error saving equations to the database.")

    def get_saved_names(self):
        """
        Get a list of distinct names from the 'Equations' table.

        Returns:
            list: A list of distinct names.
        """
        if self.db is None:
            self.connect()
        try:
            with self.db:
                cursor = self.db.cursor()
                cursor.execute('SELECT DISTINCT name FROM Equations')
                return [row[0] for row in cursor.fetchall()]
        except sqlite3.Error:
            self.view.show_message("Error getting saved names.")
            return []

    def load_history(self, name):
        """
        Load equations and results from the 'Equations' table based on the provided name.

        Args:
            name (str): The name associated with the history entry.
        Returns:
            list: A list of tuples containing equation and result pairs.
        """
        try:
            with self.db:
                cursor = self.db.execute(
                    'SELECT equation, result FROM Equations WHERE name = ? ORDER BY id',
                    (name,)
                )
                print("History loaded")
                return cursor.fetchall()
        except sqlite3.Error:
            self.view.show_message("Error loading equations from the database.")
            return []

    def delete_by_name(self, name):
            """
            Delete history entries from the 'Equations' table based on the provided name.
            
            Args:
                name (str): The name associated with the history entry to be deleted.
            """
            try:
                with self.db:
                    self.db.execute(
                        'DELETE FROM Equations WHERE name = ?',
                        (name,)
                    )
                    self.db.commit()
            except sqlite3.Error:
                self.view.show_message("Error deleting history from the database.")

    def clear_history(self):
        """Clear all records from the 'Equations' table."""
        try:
            with self.db:
                self.db.execute('DELETE FROM Equations')
                self.db.commit()
                print("Database cleared.")
        except sqlite3.Error:
            self.view.show_message("Error clearing the database.")

    def close_connection(self):
        """Close the connection to the SQLite database."""
        self.db.close()
        self.db = None
