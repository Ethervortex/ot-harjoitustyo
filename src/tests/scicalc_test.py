import unittest
from tkinter import Tk
from ui import CalcUI

class TestSciCalc(unittest.TestCase):
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
        self.ui._controller.press('=')
        equation = self.ui._controller.equation.get()
        self.assertEqual(equation, 'No expression to evaluate')
        self.ui._controller.equation.set('7 + (')
        self.ui._controller.press('=')
        equation = self.ui._controller.equation.get()
        self.assertIn('Error: ', equation)
        self.ui._controller.equation.set('1 / 0')
        self.ui._controller.press('=')
        equation = self.ui._controller.equation.get()
        self.assertIn('Error: ', equation)
        self.ui._controller.equation.set('cov(0.5)')
        self.ui._controller.press('=')
        equation = self.ui._controller.equation.get()
        self.assertIn('Error: ', equation)

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
        self.ui._controller.press('\u232b')
        self.ui._controller.press('\u232b')
        self.ui._controller.press('\u232b')
        equation = self.ui._controller.equation.get()
        self.assertEqual(equation, '5 * (1 ')
        self.ui._controller.equation.set('6')
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
