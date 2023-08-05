from kabaret import flow

class ClearMapAction(flow.Action):
    """
    Clears all map's items.
    """
    ICON = ('icons.gui', 'remove-symbol')

    _map = flow.Parent()

    def needs_dialog(self):
        return False

    def run(self, button):
        self._map.clear()
        self._map.touch()
