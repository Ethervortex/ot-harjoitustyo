from tkinter import StringVar
from math import (
    log10, log, sqrt, pi, exp, factorial, floor, sin, cos, tan,
    asin, acos, atan, radians, degrees
)
from fractions import Fraction
from scicalc_db import SciCalcDatabase

class SciCalcController:
    def __init__(self, view):
        self.view = view
        self.equation = StringVar(value='')
        self.result_available = False
        self.radians = True
        self.previous_equations = []
        self.database = SciCalcDatabase()

    def press(self, button_text):
        button_functions = {
            '=': self._evaluate,
            'C': self._clear,
            'radians': self._angle_units,
            '\u232b': self._backspace,
            '\u2bc7': lambda: self._move_cursor('\u2bc7'),
            '\u2bc8': lambda: self._move_cursor('\u2bc8'),
            '+': lambda: self._basic_operations('+'),
            '-': lambda: self._basic_operations('-'),
            '\u00d7': lambda: self._basic_operations('\u00d7'),
            '\u00F7': lambda: self._basic_operations('\u00F7'),
            '.': lambda: self._basic_operations('.'),
            '(': lambda: self._basic_operations('('),
            ')': lambda: self._basic_operations(')'),
            '\u00b1': self._negate,
            '\u03c0': lambda: self._constants('\u03c0'),
            'e': lambda: self._constants('e'),
            'sin': lambda: self._trigonometry('sin'),
            'cos': lambda: self._trigonometry('cos'),
            'tan': lambda: self._trigonometry('tan'),
            'sin\u207B\u00B9': lambda: self._trigonometry('sin\u207B\u00B9'),
            'cos\u207B\u00B9': lambda: self._trigonometry('cos\u207B\u00B9'),
            'tan\u207B\u00B9': lambda: self._trigonometry('tan\u207B\u00B9'),
            'x\u00b2': lambda: self._exponents('x\u00b2'),
            'x\u02B8': lambda: self._exponents('x\u02B8'),
            '10\u02E3': lambda: self._exponents('10\u02E3'),
            'e\u02E3': lambda: self._exponents('e\u02E3'),
            '\u221ax': lambda: self._roots('\u221ax'),
            '\u230Ax\u230B': self._floor,
            'log': lambda: self._logarithms('log'),
            'ln': lambda: self._logarithms('ln'),
            'x!': self._factorials,
            'mod': self._modulus,
            'abs': lambda: self._absolute('abs'),
            'a/b': self._fractions,
            '\u21b6': lambda: self._undo_redo('undo'),
            '\u21b7': lambda: self._undo_redo('redo'),
            **{str(i): lambda digit=i: self._basic_operations(str(digit)) for i in range(10)}
        }
        button_functions[button_text]()

    def _handle_error(self, error_message):
        self.equation.set(error_message)
        self.result_available = False
        self.view.update_button_state()

    def _evaluate(self):
        print('equation_string:', self.equation.get())
        if not self.equation.get().strip():
            self._handle_error("No expression to evaluate")
            return
        try:
            result = self._safe_eval(self.equation.get())
            self.result_available = True
            self.view.update_button_state()
            self.previous_equations.append((self.equation.get(), result))
            self.equation.set(result)
            print('Previous equations:', self.previous_equations)
            self.view.move_cursor(len(str(result)) - self.view.get_cursor_position())
        except (SyntaxError, ValueError, ZeroDivisionError, NameError, TypeError) as e:
            self._handle_error(f"Error: {e}")
        except Exception as e:
            self._handle_error("An unexpected error occurred")

    def _safe_eval(self, equation):
        safe_functions = {
            'sin': sin,
            'cos': cos,
            'tan': tan,
            'asin': asin,
            'acos': acos,
            'atan': atan,
            'radians': radians,
            'degrees': degrees,
            'log10': log10,
            'log': log,
            'sqrt': sqrt,
            'pi': pi,
            'exp': exp,
            'floor': floor,
            'factorial': factorial
        }
        return eval(equation, {}, safe_functions)

    def _clear(self):
        self.equation.set('')
        self.result_available = False
        self.view.update_button_state()

    def _angle_units(self):
        self.view.update_angle_units()

    def _backspace(self):
        self.result_available = False
        self.view.update_button_state()
        current_equation = self.equation.get()
        if current_equation:
            last_space = current_equation.rfind(' ')
            if last_space == -1:
                new_equation = current_equation[:-1]
            else:
                print('length:', len(current_equation)-1, 'last_space:', last_space)
                if last_space == len(current_equation)-1:
                    new_equation = current_equation[:-2]
                else:
                    new_equation = current_equation[:-1]
            self.equation.set(new_equation)
        else:
            self.equation.set('')

    def _move_cursor(self, button_text):
        if button_text == '\u2bc7':
            self.view.move_cursor(-1)
        else:
            self.view.move_cursor(1)

    def _insert_at_cursor(self, text_to_insert):
        cursor_position = self.view.get_cursor_position()
        current_text = self.equation.get()
        new_text = current_text[:cursor_position] + text_to_insert + current_text[cursor_position:]
        self.equation.set(new_text)
        move = len(text_to_insert)
        self.view.move_cursor(move)

    def _basic_operations(self, button_text):
        if button_text in {'\u00d7', '\u00F7'}:
            button_text = ' * ' if button_text == '\u00d7' else ' / '
        elif button_text in {'+', '-'}:
            button_text = f' {button_text} '
        self._insert_at_cursor(button_text)

    def _negate(self):
        cursor_position = self.view.get_cursor_position()
        equation = self.equation.get()
        negated_number = ''
        start_index = cursor_position
        while start_index > 0 and (equation[start_index - 1].isdigit()
                                   or equation[start_index - 1] == '.'
                                   or equation[start_index - 1] == '-'):
            start_index -= 1

        end_index = cursor_position
        while end_index < len(equation) and (equation[end_index].isdigit()
                                             or equation[end_index] == '.'):
            end_index += 1

        current_number = equation[start_index:end_index]
        negated_number = '-' + current_number if not current_number.startswith('-') else current_number[1:]
        new_equation = equation[:start_index] + negated_number + equation[end_index:]
        move = 1 if negated_number and negated_number[0] == '-' else -1
        if cursor_position == len(equation):
            move = 1

        self.equation.set(new_equation)
        self.view.move_cursor(move)

    def _constants(self, button_text):
        if button_text == 'e':
            button_text = str(exp(1))
        else:
            button_text = str(pi)
        #new_equation = self.equation.get() + button_text
        #self.equation.set(new_equation)
        self._insert_at_cursor(button_text)

    def _trigonometry(self, button_text):
        if self.radians:
            if button_text in {'sin', 'cos', 'tan'}:
                button_text += '('
            else:
                button_text = 'a' + button_text[0:3] + '('
        else:
            if button_text in {'sin', 'cos', 'tan'}:
                button_text += '(radians('
            else:
                button_text = 'degrees(a' + button_text[0:3] + '('
        self._insert_at_cursor(button_text)
        #new_equation = self.equation.get() + button_text
        #self.equation.set(new_equation)

    def _exponents(self, button_text):
        if button_text == 'x\u00B2':
            button_text = ' ** 2'
        elif button_text == 'x\u02B8':
            button_text = ' ** '
        elif button_text == '10\u02E3':
            button_text = '10 ** '
        else:
            button_text =  'exp('
        self._insert_at_cursor(button_text)
        #new_equation = self.equation.get() + button_text
        #self.equation.set(new_equation)

    def _logarithms(self, button_text):
        if button_text == 'log':
            button_text = 'log10' + '('
        else:
            button_text = 'log' + '('
        self._insert_at_cursor(button_text)
        #new_equation = self.equation.get() + button_text
        #self.equation.set(new_equation)

    def _roots(self, button_text):
        button_text = 'sqrt' + '('
        self._insert_at_cursor(button_text)
        #new_equation = self.equation.get() + button_text
        #self.equation.set(new_equation)

    def _factorials(self):
        self._insert_at_cursor('factorial(')
        #new_equation = self.equation.get() + 'factorial('
        #self.equation.set(new_equation)

    def _modulus(self):
        self._insert_at_cursor('%')
        #new_equation = self.equation.get() + '%'
        #self.equation.set(new_equation)

    def _absolute(self, button_text):
        self._insert_at_cursor(button_text + '(')
        #new_equation = self.equation.get() + button_text + '('
        #self.equation.set(new_equation)

    def _floor(self):
        self._insert_at_cursor('floor(')
        #new_equation = self.equation.get() + 'floor('
        #self.equation.set(new_equation)

    def _fractions(self):
        if self.result_available:
            result = self.equation.get()
            try:
                fraction_result = Fraction(result).limit_denominator()
                self.equation.set(fraction_result)
                self.view.move_cursor(len(str(fraction_result)) - self.view.get_cursor_position())
            except ValueError:
                self.equation.set("Conversion error")

    def _undo_redo(self, action):
        if action == 'undo':
            print('undo')
        elif action == 'redo':
            print('redo')
