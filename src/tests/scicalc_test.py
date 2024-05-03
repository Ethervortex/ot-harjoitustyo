import unittest
from unittest.mock import patch, MagicMock
from tkinter import Tk
from ui.ui import CalcUI

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
        self.ui._controller.equation.set("'hello' + 5")
        self.ui._controller.press('=')
        equation = self.ui._controller.equation.get()
        self.assertEqual(equation, 'Error during evaluation.')

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

    def test_floor(self):
        self.ui._controller.press('\u230Ax\u230B')
        equation = self.ui._controller.equation.get()
        self.assertEqual(equation, 'floor(')

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
