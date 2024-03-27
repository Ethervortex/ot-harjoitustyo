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
            print('test symbols:', '\u00b2', '\u03c0', '\u2bc7', '\u140a', '\u21b6', '\u2ba8', 
                  '\u2190', '\u2b60', '\u221a', '\u232b', ' x\u207B\u00B9', 'x\u02B8', 'e\u02E3')
            try:
                result = eval(self.equation_string)
                self.equation.set(result)
                self.equation_string = str(result)
            except Exception as e:
                print(f"Error: {e}")
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
