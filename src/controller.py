from tkinter import StringVar
from math import pi, exp

class SciCalcController:
    def __init__(self, view):
        self.view = view
        self.equation = StringVar(value='0')
        self.equation_string = ''
        self.all_equations = []

    def press(self, button_text):
        if self.equation.get() == '0':
            self.equation.set('')
            self.equation_string = ''
        if button_text == '=':
            self._evaluate()
        elif button_text == 'C':
            self._clear()
        elif button_text in {'+', '-', '\u00d7', '\u00F7', '.', '(', ')'} or button_text.isdigit():
            self._basic_operations(button_text)
        elif button_text == '\u00b1':
            self._negate()
        elif button_text in {'\u03c0', 'e'}:
            self._constants(button_text)
        else:
            self._functions(button_text)

    def _evaluate(self):
        print('equation_string:', self.equation_string)
        try:
            result = eval(self.equation_string)
            self.equation.set(result)
            self.equation_string = str(result)
        except SyntaxError:
            self.equation.set("Syntax error")
            self.equation_string = ''
        except ZeroDivisionError:
            self.equation.set("Division by zero error")
            self.equation_string = ''

    def _clear(self):
        self.equation.set('0')
        self.equation_string = ''

    def _basic_operations(self, button_text):
        if button_text in {'\u00d7', '\u00F7'}:
            button_text = ' * ' if button_text == '\u00d7' else ' / '
        elif button_text in {'+', '-'}:
            button_text = f' {button_text} '
        self.equation_string += button_text
        new_equation = self.equation.get() + button_text
        self.equation.set(new_equation)

    def _negate(self):
        equation = self.equation.get()
        last_space = equation.rfind(' ')
        last_parenthesis = equation.rfind('(')
        position = max(last_space, last_parenthesis)

        if position == -1:
            new_equation = '-' + equation if not equation.startswith('-') else equation[1:]
        else:
            last_number = equation[position + 1:]
            new_equation = equation[:position + 1] + ('-' + last_number if not last_number.startswith('-') else last_number[1:])

        self.equation.set(new_equation)
        self.equation_string = new_equation

    def _constants(self, button_text):
        if button_text == 'e':
            button_text = str(exp(1))
        else:
            button_text = str(pi)
        self.equation_string += button_text
        new_equation = self.equation.get() + button_text
        self.equation.set(new_equation)

    def _functions(self, button_text):
        button_text = f' {button_text} '
        self.equation_string += button_text
        new_equation = self.equation.get() + button_text
        self.equation.set(new_equation)
