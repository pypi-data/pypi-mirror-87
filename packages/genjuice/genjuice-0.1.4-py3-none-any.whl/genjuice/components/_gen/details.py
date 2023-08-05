# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Details(Component):
    """
    The HTML Details Element (<details>) creates a disclosure widget in which information is visible only when the widget is toggled into an "open" state. A summary or label can be provided using the <summary> element.
    """

    def __init__(self, *slots, open=None):
        super().__init__(*slots)

        self.attr(**{"open": open})

    def render(self):
        return Component(tag_name="details").proxy(self).render()
