# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Dialog(Component):
    """
    The HTML <dialog> element represents a dialog box or other interactive component, such as a dismissable alert, inspector, or subwindow.
    """

    def __init__(self, *slots, open=None):
        super().__init__(*slots)

        self.attr(**{"open": open})

    def render(self):
        return Component(tag_name="dialog").proxy(self).render()
