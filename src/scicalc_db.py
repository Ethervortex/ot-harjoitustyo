import sqlite3
from contextlib import contextmanager

class SciCalcDatabase:
    def __init__(self, db_path='calculator.db'):
        self.db_path = db_path
        self.connection = None
        self.cursor = None
        self._create_table()

    def _create_table(self):
        with self._get_cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS equations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    equation TEXT
                )
            ''')

    @contextmanager
    def _get_cursor(self):
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_path)
        cursor = self.connection.cursor()
        try:
            yield cursor
        finally:
            cursor.close()

    def close_connection(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None
