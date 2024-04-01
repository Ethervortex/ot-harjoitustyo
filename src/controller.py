from tkinter import StringVar

class SciCalcController:
    def __init__(self, view):
        self.view = view
        self.equation = StringVar()
        self.equation_string = ''
        self.all_equations = []

    def press(self, button_text):
        if button_text == '=':
            print('equation_string:', self.equation_string)
            print('test symbols:', '\u2bc7', '\u140a', '\u21b6', '\u2ba8',
                  '\u2190', '\u2b60', '\u221a', '\u232b')
            try:
                result = eval(self.equation_string)
                self.equation.set(result)
                self.equation_string = str(result)
            except SyntaxError as se:
                print(f"SyntaxError: {se}")
                self.equation.set("Syntax error")
                self.equation_string = ''
            except ZeroDivisionError as ze:
                print(f"ZeroDivisionError: {ze}")
                self.equation.set("Division by zero error")
                self.equation_string = ''
        else:
            if button_text in {'\u00d7', '\u00F7'}:
                self.equation_string += ' * ' if button_text == '\u00d7' else ' / '
                button_text = f' {button_text} '
            elif not (button_text.isdigit() or button_text == '.'):
                button_text = f' {button_text} '
                self.equation_string += button_text
            else:
                self.equation_string += button_text

            new_equation = self.equation.get() + button_text
            self.equation.set(new_equation)
