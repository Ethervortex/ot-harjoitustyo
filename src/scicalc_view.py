from tkinter import ttk, constants

class SciCalcView:

    def __init__(self, root, controller):
        self._root = root
        self._controller = controller
        self._frame = None
        self._buttons_widgets = []
        self._buttons = [
            'radians', '\u21b6', '\u21b7', '\u2bc7', '\u2bc8', '\u232b', 'C',
            'sin', 'cos', 'tan', '\u03c0', '(', ')', '\u00b1', '÷',
            'sin\u207B\u00B9', 'cos\u207B\u00B9', 'tan\u207B\u00B9', 'e', '7', '8', '9', '×',
            'x\u00b2', 'x\u02B8', '\u221ax', '\u230Ax\u230B', '4', '5', '6', '-',
            'log', 'ln', '10\u02E3', 'e\u02E3', '1', '2', '3', '+',
            'x!', 'mod', 'abs', 'a/b', '0', '.', '=',
        ]
        self._add_styles()
        self._add_widgets()
        self._arrange_widgets()
        self.update_button_state()

    def pack(self):
        self._frame.pack(fill=constants.X)

    def destroy(self):
        self._frame.destroy()

    def update_button_state(self):
        for button in self._buttons_widgets:
            if button["text"] == 'a/b':
                if self._controller.result_available:
                    button.configure(style="Fraction.TButton", state='!disabled')
                else:
                    button.configure(style="Fraction.TButton", state='disabled')

    def update_angle_units(self):
        for button in self._buttons_widgets:
            if button["text"] in {'radians', 'degrees'}:
                if button["text"] == 'radians':
                    button["text"] = 'degrees'
                    button.state(['pressed'])
                    self._controller.radians = False
                else:
                    button["text"] = 'radians'
                    button.state(['!pressed'])
                    self._controller.radians = True

    def _add_styles(self):
        style = ttk.Style()
        style.theme_use('alt')
        style.configure("MainFrame.TFrame", background='lightgrey')
        style.configure("Angle.TButton", font=('Segoe UI', 15, 'bold'), padding=(5, 5))
        style.map("Angle.TButton",
            background=[('pressed', 'lightyellow'), ('!pressed', 'yellow')])
        style.configure("Calc.TButton", font=('Segoe UI', 15, 'bold'), background='lightgrey')
        style.configure("Number.TButton", font=('Segoe UI', 16, 'bold'), background='darkgrey')
        style.configure("BasicOperation.TButton",
                        font=('Segoe UI', 16, 'bold'), background='lightgreen')
        style.configure("Equal.TButton", font=('Segoe UI', 16, 'bold'), background='#606060')
        style.configure("Clear.TButton", font=('Segoe UI', 15, 'bold'), background='red')
        style.configure("Backspace.TButton", font=('Segoe UI', 15, 'bold'), background='orange')
        style.configure("Fraction.TButton", font=('Segoe UI', 15, 'bold'), background='lightgray')
        style.map("Fraction.TButton",
            foreground=[('disabled', 'grey'), ('!disabled', 'black')],
            background=[('active', 'white'), ('disabled', 'lightgrey'), ('!disabled', 'darkgrey')])

    def _add_widgets(self):
        self._frame = ttk.Frame(master=self._root, style="MainFrame.TFrame")
        self._entry_field = ttk.Entry(
            self._frame,
            textvariable=self._controller.equation,
            justify=constants.RIGHT,
            font=('Arial', 18)
        )
        self._entry_field.focus_set()
        self._cursor_visible = True
        self._entry_field.icursor("")
        self._add_buttons()

    def _add_buttons(self):
        for button_text in self._buttons:
            button_style = (
                "Number.TButton" if button_text.isdigit() or button_text in ['.', '(', ')', '±']
                else "BasicOperation.TButton" if button_text in ['+', '-', '×', '÷']
                else "Equal.TButton" if button_text == '='
                else "Clear.TButton" if button_text == 'C'
                else "Backspace.TButton" if button_text == '\u232b'
                else "Fraction.TButton" if button_text == 'a/b'
                else "Angle.TButton" if button_text in ['radians', 'degrees']
                else "Calc.TButton"
            )
            button = ttk.Button(
                self._frame,
                text=button_text,
                style=button_style,
                width=5,
                command=lambda text=button_text: self._button_press(text)
            )
            self._buttons_widgets.append(button)

    def _arrange_widgets(self):
        self._entry_field.grid(row=0, column=0, columnspan=8,
                               pady=10, ipady=15, sticky=constants.EW)
        self._arrange_buttons()

    def _arrange_buttons(self):
        row_num, col_num = 1, 0
        for i, button in enumerate(self._buttons_widgets):
            button.grid(row=row_num, column=col_num, padx=5, pady=5, sticky=constants.NSEW)
            if i == 0:
                button.grid(columnspan=2)
                col_num += 1
            col_num += 1
            if button["text"] == '=':
                button.grid(columnspan=2)
                col_num += 1
            if col_num > 7:
                col_num = 0
                row_num += 1

    def _button_press(self, button_text):
        self._controller.press(button_text)
        self._entry_field.focus_set()
        cursor_position = len(self._entry_field.get())
        self._entry_field.icursor(cursor_position)
