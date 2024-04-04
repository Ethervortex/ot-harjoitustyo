from tkinter import StringVar
from math import log10, log, sqrt, pi, exp, factorial, floor

class SciCalcController:
    def __init__(self, view):
        self.view = view
        self.equation = StringVar(value='0')
        #self.equation_string = ''
        self.radians = True
        self.all_equations = []

    def press(self, button_text):
        if self.equation.get() == '0':
            self.equation.set('')
            #self.equation_string = ''
        if button_text == '=':
            self._evaluate()
        elif button_text == 'C':
            self._clear()
        elif button_text == '\u232b':
            self._backspace()
        elif button_text in {'\u2bc7', '\u2bc8'}:
            self._move_cursor(button_text)
        elif button_text in {'+', '-', '\u00d7', '\u00F7', '.', '(', ')'} or button_text.isdigit():
            self._basic_operations(button_text)
        elif button_text == '\u00b1':
            self._negate()
        elif button_text in {'\u03c0', 'e'}:
            self._constants(button_text)
        elif button_text in {'x\u00b2', 'x\u02B8', '10\u02E3', 'e\u02E3'}:
            self._exponents(button_text)
        elif button_text == '\u221ax':
            self._roots(button_text)
        elif button_text in {'log', 'ln'}:
            self._logarithms(button_text)
        elif button_text == 'x!':
            self._factorials()
        elif button_text == 'mod':
            self._modulus()
        elif button_text == 'abs':
            self._absolute(button_text)
        elif button_text == '\u230Ax\u230B':
            self._floor(button_text)
        else:
            self._functions(button_text)

    def _evaluate(self):
        print('equation_string:', self.equation.get())
        try:
            #result = eval(self.equation_string)
            result = self._safe_eval(self.equation.get())
            self.equation.set(result)
            #self.equation_string = str(result)
        except SyntaxError:
            self.equation.set("Syntax error")
            #self.equation_string = ''
        except ZeroDivisionError:
            self.equation.set("Division by zero error")
            #self.equation_string = ''

    def _safe_eval(self, equation):
        safe_functions = {
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
        self.equation.set('0')
        #self.equation_string = ''
    
    def _backspace(self):
        current_equation = self.equation.get()
        if current_equation:
            last_space = current_equation.rfind(' ')
            if last_space == -1:
                new_equation = current_equation[:-1]
            else:
                new_equation = current_equation[:last_space]
            self.equation.set(new_equation)
        else:
            self.equation.set('0')

    def _move_cursor(self, button_text):
        if button_text == '\u2bc7':
            pass
        else:
            pass

    def _basic_operations(self, button_text):
        if button_text in {'\u00d7', '\u00F7'}:
            button_text = ' * ' if button_text == '\u00d7' else ' / '
        elif button_text in {'+', '-'}:
            button_text = f' {button_text} '
        #self.equation_string += button_text
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
        #self.equation_string = new_equation

    def _constants(self, button_text):
        if button_text == 'e':
            button_text = str(exp(1))
        else:
            button_text = str(pi)
        #self.equation_string += button_text
        new_equation = self.equation.get() + button_text
        self.equation.set(new_equation)

    def _trigonometry(self, button_text):
        pass

    def _exponents(self, button_text):
        if button_text == 'x\u00B2':
            button_text = ' ** 2'
        elif button_text == 'x\u02B8':
            button_text = ' ** '
        elif button_text == '10\u02E3':
            button_text = '10 ** '
        else:
            button_text =  'exp('
        new_equation = self.equation.get() + button_text
        self.equation.set(new_equation)

    def _logarithms(self, button_text):
        if button_text == 'log':
            button_text = 'log10' + '('
        else:
            button_text = 'log' + '('
        new_equation = self.equation.get() + button_text
        self.equation.set(new_equation)

    def _roots(self, button_text):
        button_text = 'sqrt' + '('
        #self.equation_string += button_text
        new_equation = self.equation.get() + button_text
        self.equation.set(new_equation)

    def _factorials(self):
        new_equation = self.equation.get() + 'factorial('
        self.equation.set(new_equation)

    def _modulus(self):
        #self.equation_string += '%'
        new_equation = self.equation.get() + '%'
        self.equation.set(new_equation)

    def _absolute(self, button_text):
        #self.equation_string += button_text + '('
        new_equation = self.equation.get() + button_text + '('
        self.equation.set(new_equation)

    def _floor(self, button_text):
        new_equation = self.equation.get() + 'floor('
        self.equation.set(new_equation)

    def _functions(self, button_text):
        button_text = f' {button_text} '
        #self.equation_string += button_text
        new_equation = self.equation.get() + button_text
        self.equation.set(new_equation)
