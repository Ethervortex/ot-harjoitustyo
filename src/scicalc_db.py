import sqlite3

class SciCalcDatabase:
    def __init__(self, db_path='calculator.db'):
        self.db_path = db_path
        self.connection = None

    def connect(self):
        self.connection = sqlite3.connect(self.db_path)
        self._create_table()

    def _create_table(self):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS equations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    equation TEXT
                )
            ''')

    def close_connection(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None
