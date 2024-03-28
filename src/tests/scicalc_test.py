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
        self.assertEqual(self.ui._controller.equation_string, ' * ')

    def test_divide_press(self):
        self.ui._controller.press('\u00F7')
        self.assertEqual(self.ui._controller.equation_string, ' / ')

    def test_digit_press(self):
        self.ui._controller.press('5')
        self.assertEqual(self.ui._controller.equation_string, '5')
