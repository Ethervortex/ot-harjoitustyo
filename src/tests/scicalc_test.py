import unittest
import sqlite3
from unittest.mock import patch, MagicMock
from tkinter import Tk
from ui.ui import CalcUI
from repositories.scicalc_db import SciCalcDatabase
import io
from build import build
from config import DATABASE_FILE_PATH
import os

class TestSciCalcController(unittest.TestCase):
    def setUp(self):
        self.window = Tk()
        self.ui = CalcUI(self.window)
        self.ui.start()
        self.controller = self.ui._controller

    def tearDown(self):
        self.window.destroy()

    def test_multiply_press(self):
        self.ui._controller.press('\u00d7')
        equation = self.ui._controller.equation.get()
        self.assertEqual(equation, ' * ')

    def test_divide_press(self):
        self.ui._controller.press('\u00F7')
        equation = self.ui._controller.equation.get()
        self.assertEqual(equation, ' / ')

    def test_plus_press(self):
        self.ui._controller.press('+')
        equation = self.ui._controller.equation.get()
        self.assertEqual(equation, ' + ')

    def test_minus_press(self):
        self.ui._controller.press('-')
        equation = self.ui._controller.equation.get()
        self.assertEqual(equation, ' - ')

    def test_digit_press(self):
        self.ui._controller.press('5')
        equation = self.ui._controller.equation.get()
        self.assertEqual(equation, '5')

    def test_errors(self):
        self.ui._controller.equation.set('7 + ')
        self.ui._controller.press('=')
        equation = self.ui._controller.equation.get()
        self.assertEqual(equation, 'Syntax error')
        self.ui._controller.equation.set('1 / 0')
        self.ui._controller.press('=')
        equation = self.ui._controller.equation.get()
        self.assertEqual(equation, 'Division by zero error')
        self.ui._controller.equation.set('cov(0.5)')
        self.ui._controller.press('=')
        equation = self.ui._controller.equation.get()
        self.assertEqual(equation, 'Argument error')
        self.ui._controller.equation.set('acos(6) * asin(5)')
        self.ui._controller.press('=')
        equation = self.ui._controller.equation.get()
        self.assertEqual(equation, 'Value error')

    @patch('tkinter.messagebox.showerror')
    def test_messagebox(self, mock_message):
        self.ui._controller.equation.set('')
        self.ui._controller.press('=')
        mock_message.assert_called_with("Error", "No expression to evaluate")
        self.ui._controller.equation.set('(1')
        self.ui._controller.press('=')
        mock_message.assert_called_with("Error", "Unmatched parentheses")

    def test_check_parentheses(self):
        equation = ')'
        result = self.ui._controller._check_parentheses(equation)
        self.assertTrue(result)

    def test_evaluate(self):
        self.ui._controller.equation.set('5 * (1 + 2)')
        self.ui._controller.press('=')
        equation = self.ui._controller.equation.get()
        self.assertEqual(equation, '15')

    def test_clear(self):
        self.ui._controller.press('C')
        equation = self.ui._controller.equation.get()
        self.assertEqual(equation, '')

    def test_backspace(self):
        self.ui._controller.equation.set('5 * (1 + 2)')
        self.ui._view.move_cursor(len('5 * (1 + 2)'))
        self.ui._controller.press('\u232b')
        self.ui._controller.press('\u232b')
        self.ui._controller.press('\u232b')
        equation = self.ui._controller.equation.get()
        self.assertEqual(equation, '5 * (1 +')
        self.ui._controller.equation.set('6')
        self.ui._view.move_cursor(1)
        self.ui._controller.press('\u232b')
        self.ui._controller.press('\u232b')
        equation = self.ui._controller.equation.get()
        self.assertEqual(equation, '')

    def test_angle_units(self):
        self.ui._controller.press('radians')
        units = self.ui._controller.radians
        self.assertEqual(units, False)

    def test_negate(self):
        self.ui._controller.equation.set('10')
        self.ui._controller.press('\u00b1')
        equation = self.ui._controller.equation.get()
        self.assertEqual(equation, '-10')
        self.ui._controller.equation.set('5 + 6')
        self.ui._view.move_cursor(5)
        self.ui._controller.press('\u00b1')
        equation = self.ui._controller.equation.get()
        self.assertEqual(equation, '5 + -6')

    def test_constants(self):
        self.ui._controller.press('e')
        equation = self.ui._controller.equation.get()
        self.assertAlmostEqual(float(equation), 2.718, places=3)
        self.ui._controller.equation.set('')
        self.ui._controller.press('\u03c0')
        equation = self.ui._controller.equation.get()
        self.assertAlmostEqual(float(equation), 3.14159, places=5)

    def test_move_cursor(self):
        self.ui._controller.equation.set('12345')
        self.ui._view.move_cursor(len('12345'))
        self.ui._controller.press('\u2bc7')
        self.ui._controller.press('\u2bc7')
        self.ui._controller.press('\u2bc8')
        position = self.ui._view.get_cursor_position()
        self.assertEqual(position, 4)

    def test_trigonometry(self):
        self.ui._controller.press('sin')
        equation = self.ui._controller.equation.get()
        self.assertEqual(equation, 'sin(')
        self.ui._controller.equation.set('')
        self.ui._controller.press('cos\u207B\u00B9')
        equation = self.ui._controller.equation.get()
        self.assertEqual(equation, 'acos(')
        self.ui._controller.equation.set('')
        self.ui._controller.press('radians')
        self.ui._controller.press('tan')
        equation = self.ui._controller.equation.get()
        self.assertEqual(equation, 'tan(radians(')
        self.ui._controller.equation.set('')
        self.ui._controller.press('sin\u207B\u00B9')
        equation = self.ui._controller.equation.get()
        self.assertEqual(equation, 'degrees(asin(')

    def test_exponents(self):
        self.ui._controller.press('x\u00B2')
        equation = self.ui._controller.equation.get()
        self.assertEqual(equation, ' ** 2')
        self.ui._controller.equation.set('')
        self.ui._controller.press('x\u02B8')
        equation = self.ui._controller.equation.get()
        self.assertEqual(equation, ' ** ')
        self.ui._controller.equation.set('')
        self.ui._controller.press('10\u02E3')
        equation = self.ui._controller.equation.get()
        self.assertEqual(equation, '10 ** ')
        self.ui._controller.equation.set('')
        self.ui._controller.press('e\u02E3')
        equation = self.ui._controller.equation.get()
        self.assertEqual(equation, 'exp(')

    def test_logarithms(self):
        self.ui._controller.press('log')
        equation = self.ui._controller.equation.get()
        self.assertEqual(equation, 'log10(')
        self.ui._controller.equation.set('')
        self.ui._controller.press('ln')
        equation = self.ui._controller.equation.get()
        self.assertEqual(equation, 'log(')

    def test_roots(self):
        self.ui._controller.press('\u221ax')
        equation = self.ui._controller.equation.get()
        self.assertEqual(equation, 'sqrt(')

    def test_factorials(self):
        self.ui._controller.press('x!')
        equation = self.ui._controller.equation.get()
        self.assertEqual(equation, 'factorial(')

    def test_modulus(self):
        self.ui._controller.press('mod')
        equation = self.ui._controller.equation.get()
        self.assertEqual(equation, '%')

    def test_absolute(self):
        self.ui._controller.press('abs')
        equation = self.ui._controller.equation.get()
        self.assertEqual(equation, 'abs(')

    def test_fractions(self):
        self.ui._controller.equation.set('2.5')
        self.ui._controller.press('=')
        self.ui._controller.result_available = True
        self.ui._controller.press('a/b')
        equation = self.ui._controller.equation.get()
        self.assertEqual(equation, '5/2')
        self.ui._controller.press('(')
        self.ui._controller.press('a/b')
        equation = self.ui._controller.equation.get()
        self.assertEqual(equation, 'Conversion error')
        self.ui._controller.press('C')
        self.ui._controller.press('a/b')
        equation = self.ui._controller.equation.get()
        self.assertEqual(equation, '')

    def test_undo_redo(self):
        self.ui._controller.press('\u21b6')
        self.assertEqual(self.ui._controller.history_index, -1)
        self.ui._controller.press('\u21b7')
        equation = self.ui._controller.equation.get()
        self.assertEqual(equation, '')
        self.ui._controller.equation.set('10 + 2')
        self.ui._controller.press('=')
        self.ui._controller.press('\u21b6')
        equation = self.ui._controller.equation.get()
        self.assertEqual(equation, '10 + 2')
        self.ui._controller.press('\u21b7')
        self.ui._controller.equation.set('6 * 6')
        self.ui._controller.press('=')
        self.ui._controller.equation.set('sqrt(4)')
        self.ui._controller.press('=')
        self.ui._controller.press('\u21b6')
        self.ui._controller.press('\u21b6')
        equation = self.ui._controller.equation.get()
        self.assertEqual(equation, '6 * 6')

    def test_memory(self):
        self.ui._controller.press('MS')
        self.assertIsNone(self.ui._controller.memory)
        self.ui._controller.press('MR')
        self.assertEqual(self.ui._controller.equation.get(), '')
        self.ui._controller.press('1')
        self.ui._controller.press('+')
        self.ui._controller.press('1')
        self.ui._controller.press('=')
        self.ui._controller.press('MS')
        self.assertEqual(self.ui._controller.memory, '2')
        self.ui._controller.equation.set('')
        self.ui._controller.press('MR')
        self.assertEqual(self.ui._controller.memory, '2')

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
