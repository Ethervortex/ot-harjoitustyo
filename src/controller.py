from tkinter import StringVar, messagebox, simpledialog
from math import (
    log10, log, sqrt, pi, exp, factorial, floor, sin, cos, tan,
    asin, acos, atan, radians, degrees
)
from fractions import Fraction
from scicalc_db import SciCalcDatabase

class SciCalcController:
    """
    Controller class for the scientific calculator. This class handles user interactions and
    control logic of the scientific calculator.

    Attributes:
        view (SciCalcView): The associated GUI.
    """
    def __init__(self, view):
        """Initialize the SciCalcController.

        Args:
            view (SciCalcView): The associated view.
        """
        self.view = view
        self.equation = StringVar(value='')
        self.result_available = False
        self.radians = True
        self.history = []
        self.history_index = -1
        self.database = SciCalcDatabase()
        self.memory = None

    def press(self, button_text):
        """Handle button press.

        Args:
            button_text (str): The text of the pressed button.
        """
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
            **{str(i): lambda digit=i: self._basic_operations(str(digit)) for i in range(10)},
            'Save': self.history_db_save,
            'Load': self.history_db_load,
            'Clear': self.history_db_clear,
            'MS': lambda: self._memory('MS'),
            'MR': lambda: self._memory('MR')
        }
        button_functions[button_text]()

    def evaluate_expression(self):
        """Evaluate the current expression."""
        self._evaluate()

    def _handle_error(self, error_message):
        """Handle and show errors.

        Args:
             (str): The error message to show.
        """
        self.equation.set(error_message)
        self.result_available = False
        self.view.move_cursor(len(str(error_message)) - self.view.get_cursor_position())
        self.view.update_button_state()

    def show_message(self, message):
        """Show a message box with an error message.

        Args:
            message (str): The message to display.
        """
        messagebox.showerror("Error", message)

    def _check_parentheses(self, equation):
        """Check for unmatched parentheses in the equation.

        Args:
            equation (str): The equation to check.
        """
        parantheses = []
        for char in equation:
            if char == '(':
                parantheses.append(char)
            elif char == ')':
                if not parantheses:
                    return True
                parantheses.pop()
        return bool(parantheses)

    def _update_history_list(self, equation, result):
        """Update the history list with the current equation and result.

        Args:
            equation (str): The current equation.
            result: The result of the evaluation."""
        self.view.update_button_state()
        self.history = self.history[:self.history_index + 1]
        self.history.append((equation, result))
        self.history_index = len(self.history) - 1
        self.view.update_history_view(self.history)

    def _evaluate(self):
        """Evaluate the current equation and handle errors."""
        equation = self.equation.get().strip()
        if self._check_parentheses(equation):
            self.show_message("Unmatched parentheses")
            return
        if not equation:
            self.show_message("No expression to evaluate")
            return
        try:
            result = self._safe_eval(self.equation.get())
            self.result_available = True
            self._update_history_list(equation, result)
            self.equation.set(result)
            self.view.move_cursor(len(str(result)) - self.view.get_cursor_position())

        except SyntaxError:
            self._handle_error("Syntax error")
        except ZeroDivisionError:
            self._handle_error("Division by zero error")
        except NameError:
            self._handle_error("Argument error")
        except ValueError:
            self._handle_error("Value error")

    def _safe_eval(self, equation):
        """Define safe functions and safely evaluate the mathematical expression.

        Args:
            equation (str): The expression to evaluate.
        """
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
        """Clear the current equation."""
        self.equation.set('')
        self.result_available = False
        self.view.update_button_state()

    def _angle_units(self):
        """Change angle units (radians/degrees)."""
        self.view.update_angle_units()

    def _backspace(self):
        """Handle the backspace button press."""
        self.result_available = False
        self.view.update_button_state()
        current_equation = self.equation.get()
        if current_equation:
            cursor_position = self.view.get_cursor_position()
            to_cursor = current_equation[:cursor_position]
            new_equation = to_cursor[:-1] + current_equation[cursor_position:]
            self.view.move_cursor(-1)
            self.equation.set(new_equation)
        else:
            self.equation.set('')

    def _move_cursor(self, button_text):
        """Handle the cursor moving buttons (left/right)
        
        Args:
            button_text (str): The text of the pressed button.
        """
        if button_text == '\u2bc7':
            self.view.move_cursor(-1)
        else:
            self.view.move_cursor(1)

    def _insert_at_cursor(self, text_to_insert):
        """Insert text at the current cursor position.

        Args:
            text_to_insert (str): The text to insert.
        """
        cursor_position = self.view.get_cursor_position()
        current_text = self.equation.get()
        new_text = current_text[:cursor_position] + text_to_insert + current_text[cursor_position:]
        self.equation.set(new_text)
        move = len(text_to_insert)
        self.view.move_cursor(move)

    def _basic_operations(self, button_text):
        """Handle basic arithmetic operations (*, /, + and -).

        Args:
            button_text (str): The text of the pressed button.
        """
        if button_text in {'\u00d7', '\u00F7'}:
            button_text = ' * ' if button_text == '\u00d7' else ' / '
        elif button_text in {'+', '-'}:
            button_text = f' {button_text} '
        self._insert_at_cursor(button_text)

    def _negate(self):
        """Negate the current number."""
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
        negated_number = (
            '-' + current_number
        ) if not current_number.startswith('-') else current_number[1:]
        new_equation = equation[:start_index] + negated_number + equation[end_index:]
        move = 1 if negated_number and negated_number[0] == '-' else -1
        if cursor_position == len(equation):
            move = 1

        self.equation.set(new_equation)
        self.view.move_cursor(move)

    def _constants(self, button_text):
        """Handle buttons for mathematical constants pi and e.

        Args:
            button_text (str): The text of the pressed button.
        """
        if button_text == 'e':
            button_text = str(exp(1))
        else:
            button_text = str(pi)
        self._insert_at_cursor(button_text)

    def _trigonometry(self, button_text):
        """Handle trigonometric functions.

        Args:
            button_text (str): The text of the pressed button.
        """
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

    def _exponents(self, button_text):
        """Handle exponentiation operations.

        Args:
            button_text (str): The text of the pressed button.
        """
        if button_text == 'x\u00B2':
            button_text = ' ** 2'
        elif button_text == 'x\u02B8':
            button_text = ' ** '
        elif button_text == '10\u02E3':
            button_text = '10 ** '
        else:
            button_text =  'exp('
        self._insert_at_cursor(button_text)

    def _logarithms(self, button_text):
        """Handle logarithmic operations log10 and ln.

        Args:
            button_text (str): The text of the pressed button.
        """
        if button_text == 'log':
            button_text = 'log10' + '('
        else:
            button_text = 'log' + '('
        self._insert_at_cursor(button_text)

    def _roots(self, button_text):
        """Handle operations for square root
        
        Args:
            button_text (str): The text of the pressed button.
        """
        button_text = 'sqrt' + '('
        self._insert_at_cursor(button_text)

    def _factorials(self):
        """Handle factorial operation."""
        self._insert_at_cursor('factorial(')

    def _modulus(self):
        """Handle modulus operation."""
        self._insert_at_cursor('%')

    def _absolute(self, button_text):
        """Handle absolute value operation.

        Args:
            button_text (str): The text of the pressed button.
        """
        self._insert_at_cursor(button_text + '(')

    def _floor(self):
        """Handle floor operation."""
        self._insert_at_cursor('floor(')

    def _fractions(self):
        """Convert the result to a fraction."""
        if self.result_available:
            result = self.equation.get()
            try:
                fraction_result = Fraction(result).limit_denominator()
                self.equation.set(fraction_result)
                self.view.move_cursor(len(str(fraction_result)) - self.view.get_cursor_position())
            except ValueError:
                self.equation.set("Conversion error")
                self.view.move_cursor(len(self.equation.get()) - self.view.get_cursor_position())

    def _undo_redo(self, action):
        """Undo or redo the previous operations (retrieve equations from history list).

        Args:
            action (str): 'undo' or 'redo'.
        """
        if action == 'undo':
            if self.history_index >= 0:
                equation, _ = self.history[self.history_index]
                self.equation.set(equation)
                self.view.move_cursor(len(str(equation)) - self.view.get_cursor_position())
                self.history_index -= 1
                self.history_index = max(self.history_index, 0)
                self.view.update_history_view(self.history)
        elif action == 'redo':
            if self.history_index < len(self.history) - 1:
                self.history_index += 1
                equation, _ = self.history[self.history_index]
                self.equation.set(equation)
                self.view.move_cursor(len(str(equation)) - self.view.get_cursor_position())
            else:
                self.history_index = len(self.history) - 1
            self.view.update_history_view(self.history)
        else:
            return

    def _memory(self, button_text):
        """Handle memory-related operations Memory Store and Memory Recall.
        Args:
            button_text (str): The text of the pressed button.
        """
        if button_text == 'MS':
            if self.result_available:
                self.memory = self.equation.get()
        else:
            if self.memory is not None:
                self._insert_at_cursor(str(self.memory))

    def load_history_from_db(self, name):
        """Load a saved history from the database.
        Args:
            name (str): The name of the saved history to load.
        """
        if name:
            self.database.connect()
            loaded_data = self.database.load_history(name)
            self.history = loaded_data
            self.history_index = len(loaded_data) - 1
            self.view.update_history_view(self.history)
            self.database.close_connection()

    def history_db_save(self):
        """Save the current history to the database."""
        if self.history:
            name = simpledialog.askstring("Save History", "Enter a name for the saved history:")
            if name:
                self.database.connect()
                for equation, result in self.history:
                    self.database.save_history(name, equation, result)
                self.database.close_connection()

    def history_db_load(self):
        saved_names = self.database.get_saved_names()
        if saved_names:
            self.view.create_combobox(saved_names)

    def history_db_clear(self):
        confirmation = messagebox.askokcancel(
            "Confirmation",
            "Are you sure you want to clear the database?"
            )
        if confirmation:
            self.database.connect()
            self.database.clear_history()
            self.database.close_connection()
            self.history = []
            self.history_index = -1
            self.view.update_history_view(self.history)
