from tkinter import ttk, constants, scrolledtext
import tkinter as tk

class SciCalcView:
    """This class represents the graphical user interface (GUI) for the scientific calculator.

    Attributes:
        _root (tk.Tk): The root Tkinter window.
        _controller (SciCalcController): The associated controller handling user interactions.
    """
    _BUTTONS = [
            'radians', 'MS', 'MR', '\u21b6', '\u21b7', '\u2bc7', '\u2bc8', '\u232b', 'C',
            'sin', 'cos', 'tan', '\u03c0', '(', ')', '\u00b1', '÷',
            'sin\u207B\u00B9', 'cos\u207B\u00B9', 'tan\u207B\u00B9', 'e', '7', '8', '9', '×',
            'x\u00b2', 'x\u02B8', '\u221ax', '\u230Ax\u230B', '4', '5', '6', '-',
            'log', 'ln', '10\u02E3', 'e\u02E3', '1', '2', '3', '+',
            'x!', 'mod', 'abs', 'a/b', '0', '.', '=', 
    ]

    def __init__(self, root, controller):
        """Initializes the SciCalcView.

        Args:
            root (tk.Tk): The root Tkinter window.
            controller (SciCalcController): The associated controller handling user interactions.
        """
        self._root = root
        self._controller = controller
        self._frame = None
        self._buttons_widgets = []
        self._menu_bar = None
        self._database_menu = None
        self._add_styles()
        self._add_widgets()
        self._arrange_widgets()
        self.update_button_state()

    def pack(self):
        """Packs the main frame to make the GUI visible."""
        self._frame.pack(fill=constants.X)

    def destroy(self):
        """Destroys the main frame, closing the GUI."""
        self._frame.destroy()

    def update_button_state(self):
        """Updates the state of buttons - enable or disable the button based on 
        the result or memory availability.
        """
        for button in self._buttons_widgets:
            if button["text"] in {'a/b', 'MS'}:
                if self._controller.result_available:
                    button.configure(style="Disable.TButton", state='!disabled')
                else:
                    button.configure(style="Disable.TButton", state='disabled')
            elif button["text"] == 'MR':
                if self._controller.memory is not None:
                    button.configure(style="Disable.TButton", state='!disabled')
                else:
                    button.configure(style="Disable.TButton", state='disabled')

    def update_angle_units(self):
        """Updates the angle units button text and the controller's radians attribute."""
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

    def get_cursor_position(self):
        """Gets the current cursor position in the entry field."""
        return self._entry_field.index(constants.INSERT)

    def move_cursor(self, move):
        """Moves the cursor in the entry field by the specified amount.
        
        Args: 
            move (int): The amount of steps (negative to left and positive to right)
        """
        new_cursor_position = self._entry_field.index(constants.INSERT) + move
        self._entry_field.icursor(new_cursor_position)

    def update_history_view(self, history):
        """Updates the history view with the provided list of equations and results.

        Args:
            history (List[[str, str]]): List of tuples representing equations and their results.
        """
        self._history.configure(state='normal')
        self._history.delete(1.0, tk.END)
        for i, item in enumerate(history):
            equation_text = f"[{i + 1}]\t{item[0]} = {item[1]}\n"
            self._history.insert(tk.END, equation_text)
        self._history.yview(tk.END)
        self._history.configure(state='disabled')

    def _add_styles(self):
        """Adds styles to the ttk.Style for consistent appearance."""
        style = ttk.Style()
        style.theme_use('alt')
        style.configure("MainFrame.TFrame", background='lightgrey')
        style.configure("Padded.TEntry", padding=(10, 5))
        style.configure("Angle.TButton", font=('Segoe UI', 15, 'bold'), padding=(0, 3))
        style.map("Angle.TButton",
            background=[('pressed', 'lightyellow'), ('!pressed', 'darkgrey')])
        style.configure("Calc.TButton", font=('Segoe UI', 15, 'bold'), background='lightgrey')
        style.configure("Number.TButton", font=('Segoe UI', 16, 'bold'), background='darkgrey')
        style.configure("BasicOperation.TButton",
                        font=('Segoe UI', 16, 'bold'), background='lightgreen')
        style.configure("Equal.TButton", font=('Segoe UI', 16, 'bold'), background='#606060')
        style.configure("Clear.TButton", font=('Segoe UI', 15, 'bold'), background='red')
        style.configure("Backspace.TButton", font=('Segoe UI', 15, 'bold'), background='orange')
        style.configure("Disable.TButton", font=('Segoe UI', 15, 'bold'), background='lightgray')
        style.map("Disable.TButton",
            foreground=[('disabled', 'grey'), ('!disabled', 'black')],
            background=[('active', 'white'), ('disabled', 'lightgrey'), ('!disabled', 'darkgrey')])
        style.configure("History.TButton", font=('Arial', 14), background='darkgrey')
        style.configure("Popup.TButton", font=('Arial', 14), background='lightgreen')

    def _add_widgets(self):
        """Initializes the widgets of the GUI, including labels, history view and entry field."""
        self._frame = ttk.Frame(master=self._root, style="MainFrame.TFrame")
        self._history_label = ttk.Label(self._frame, text="History:", font=('Arial', 12))
        self._history = scrolledtext.ScrolledText(
            self._frame,
            wrap=constants.WORD,
            font=('Arial', 12),
            height=5,
            padx=10
        )
        self._history.configure(state='disabled')
        self._entry_field = ttk.Entry(
            self._frame,
            textvariable=self._controller.equation,
            justify=constants.RIGHT,
            font=('Arial', 18),
            style="Padded.TEntry"
        )
        self._entry_field.bind("<Return>", lambda event: self._controller.evaluate())
        self._entry_field.focus_set()
        self._cursor_visible = True
        self._entry_field.icursor("")
        self._add_buttons()
        self._add_menus()

    def _add_buttons(self):
        """Initializes the buttons based on the _buttons list."""
        for button_text in SciCalcView._BUTTONS:
            button_style = (
                "Number.TButton" if button_text.isdigit() or button_text in ['.', '(', ')', '±']
                else "BasicOperation.TButton" if button_text in ['+', '-', '×', '÷']
                else "Equal.TButton" if button_text == '='
                else "Clear.TButton" if button_text == 'C'
                else "Backspace.TButton" if button_text == '\u232b'
                else "Disable.TButton" if button_text in ['a/b', 'MS', 'MR']
                else "Angle.TButton" if button_text in ['radians', 'degrees']
                else "History.TButton" if button_text in ['Save', 'Load', 'Clear']
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

    def _add_menus(self):
        """Adds a menubar with database-related options Save, Load and Clear."""
        self._menu_bar = tk.Menu()
        self._database_menu = tk.Menu(self._menu_bar, tearoff=False, font=('Arial', 12))
        self._database_menu.add_command(
            label="Save history",
            command=self._controller.history_db_save
        )
        self._database_menu.add_command(
            label="Load history",
            command=self._controller.history_db_load
        )
        self._database_menu.add_command(
            label="Clear database",
            command=self._controller.history_db_clear
        )
        self._menu_bar.add_cascade(label="Database", menu=self._database_menu)
        self._root.config(menu=self._menu_bar)

    def _arrange_widgets(self):
        """Arranges the widgets within the main frame, specifying their positions."""
        self._history_label.grid(row=0, column=0, columnspan=2,
                             pady=(10,0), padx=10, sticky=constants.W)
        self._history.grid(row=1, column=0, columnspan=8,
                                pady=5, padx=10, ipady=15, sticky=constants.EW)
        self._entry_field.grid(row=2, column=0, columnspan=8,
                               pady=10, padx=10, ipady=15, sticky=constants.EW)
        self._arrange_buttons()

    def _arrange_buttons(self):
        """Arranges the buttons within the main frame."""
        row_num, col_num = 3, 0
        for i, button in enumerate(self._buttons_widgets):
            button.grid(row=row_num, column=col_num, padx=5, pady=5, sticky=constants.NSEW)
            if i == 0:
                button.grid(columnspan=2)
                col_num += 7
            col_num += 1
            if button["text"] == '=':
                button.grid(columnspan=2)
                col_num += 1
            if col_num > 7:
                col_num = 0
                row_num += 1

    def _button_press(self, button_text):
        """Handles button presses by calling the corresponding controller method.

        Args:
            button_text (str): The text of the pressed button.
        """
        self._controller.press(button_text)
        self._entry_field.focus_set()

    def create_combobox(self, saved_names):
        """Creates a popup with a combobox for selecting a history entry.

        Args:
            saved_names (list): A list of saved history names.
        """
        popup = tk.Toplevel(self._root)
        popup.title("Load History")
        label = ttk.Label(popup, text="Select a history from the list:",
                          font=('Arial', 14), background='lightgrey')
        label.pack(padx=10, pady=10)
        combobox = ttk.Combobox(popup, state="readonly", values=saved_names, font=('Arial', 14))
        combobox.pack(padx=10, pady=10)
        button = ttk.Button(
            popup, text="Load",
            command=lambda: self._load_from_combobox(combobox, popup),
            style="Popup.TButton"
        )
        button.pack(pady=10)

    def _load_from_combobox(self, combobox, popup):
        """Loads the selected history from the combobox.

        Args:
            combobox (ttk.Combobox): The combobox widget containing saved history names.
            popup (tk.Toplevel): The popup window containing the combobox.
        """
        selected_name = combobox.get()
        if selected_name:
            popup.destroy()
            self._controller.load_history_from_db(selected_name)
