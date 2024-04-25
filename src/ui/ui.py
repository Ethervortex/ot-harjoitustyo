from ui.scicalc_view import SciCalcView
from services.controller import SciCalcController

class CalcUI:
    """
    This User Interface class is responsible for initializing and managing the user interface
    of the scientific calculator. It utilizes the 'SciCalcView' for the graphical user
    interface and 'SciCalcController' for handling user input and interactions.

    Attributes:
        _root: The TKinter element within which the interface is initialized.
    """
    def __init__(self, root):
        """Creates a new class responsible for the user interface.
        
        Args:
            root: A TKinter element within which the interface is initialized.
        """
        self._root = root
        self._view = None
        self._controller = SciCalcController(None)

    def start(self):
        """Starts user interface for the scientific calculator."""
        self._show_scicalc_view()

    def _show_scicalc_view(self):
        """Shows the scientific calculator."""
        self._view = SciCalcView(self._root, self._controller)
        self._controller.view = self._view
        self._view.pack()
