import unittest
import sqlite3
from build import build
from config import DATABASE_FILE_PATH
import os

class TestBuild(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        if os.path.exists(DATABASE_FILE_PATH):
            connection = sqlite3.connect(DATABASE_FILE_PATH)
            connection.close()
            build.db = None

    def test_build_script(self):
        build()
        self.assertTrue(os.path.exists(DATABASE_FILE_PATH))
        connection = sqlite3.connect(DATABASE_FILE_PATH)
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Equations';")
        table = cursor.fetchone()
        connection.close()
        self.assertIsNotNone(table)
