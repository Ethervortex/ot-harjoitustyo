from scicalc_view import SciCalcView

class calcUI:
    def __init__(self, root):
        """Creates a new class responsible for the user interface.
        
        args:
            root:
                A TKinter element within which the interface is initialized.
        """
        self._root = root
        self._view = None

    def start(self):
        """Starts user interface for scientific calculator."""
        self._show_scicalc_view()

    def _show_scicalc_view(self):
        """Shows scientific calculator."""
        self._view = SciCalcView(self._root)
        self._view.pack()
