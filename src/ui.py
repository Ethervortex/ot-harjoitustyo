from scicalc_view import SciCalcView
from controller import SciCalcController

class CalcUI:
    def __init__(self, root):
        """Creates a new class responsible for the user interface.
        
        args:
            root:
                A TKinter element within which the interface is initialized.
        """
        self._root = root
        self._view = None
        self._controller = SciCalcController(None)

    def start(self):
        """Starts user interface for scientific calculator."""
        self._show_scicalc_view()

    def _show_scicalc_view(self):
        """Shows scientific calculator."""
        self._view = SciCalcView(self._root, self._controller)
        self._controller.view = self._view
        self._view.pack()
