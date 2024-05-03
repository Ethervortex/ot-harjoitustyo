import unittest
import sqlite3
from repositories.scicalc_db import SciCalcDatabase
from unittest.mock import patch, MagicMock
import io

class TestSciCalcDatabase(unittest.TestCase):
    def setUp(self):
        self.connection = sqlite3.connect(':memory:')
        self.view_mock = MagicMock()
        self.database = SciCalcDatabase(self.view_mock, db_file=':memory:')
        self.database.connect()

    def tearDown(self):
        self.connection.close()

    def test_connect(self):
        self.assertIsNotNone(self.database.db)

    def test_connect_exception(self):
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout, patch('sqlite3.connect') as mock_connect:
            mock_connect.side_effect = sqlite3.Error("Test error")
            self.database.connect()
            printed_output = mock_stdout.getvalue().strip()
            self.assertIn("Error connecting to the database.", printed_output)

    def test_save_history(self):
        name = 'test'
        equation = '1 + 2'
        result = '3'
        self.database.save_history(name, equation, result)
        cursor = self.database.db.cursor()
        cursor.execute("SELECT * FROM Equations WHERE name=?", (name,))
        saved_history = cursor.fetchone()
        self.assertIsNotNone(saved_history)
        self.assertEqual(saved_history[1], name)
        self.assertEqual(saved_history[2], equation)
        self.assertEqual(saved_history[3], result)

    def test_get_saved_names(self):
        names = ['test1', 'test2', 'test3']
        for name in names:
            self.database.save_history(name, 'equation', 'result')
        saved_names = self.database.get_saved_names()
        self.assertEqual(sorted(saved_names), sorted(names))
        self.database.db = None
        saved_names = self.database.get_saved_names()
        self.assertIsNotNone(self.database.db)

    def test_load_history(self):
        name = 'test'
        equations = [('sqrt(4)', '2.0'), ('8 * 8', '64')]
        for equation, result in equations:
            self.database.save_history(name, equation, result)
        loaded_history = self.database.load_history(name)
        self.assertEqual(loaded_history, equations)

    def test_clear_history(self):
        self.database.save_history('test', '1 * 4', '4')
        self.database.clear_history()
        cursor = self.database.db.cursor()
        cursor.execute("SELECT COUNT(*) FROM Equations")
        count = cursor.fetchone()[0]
        self.assertEqual(count, 0)

    def test_close_connection(self):
        self.database.close_connection()
        self.assertIsNone(self.database.db)
        self.database.connect()
        self.assertIsNotNone(self.database.db)
        self.database.close_connection()
        self.assertIsNone(self.database.db)
