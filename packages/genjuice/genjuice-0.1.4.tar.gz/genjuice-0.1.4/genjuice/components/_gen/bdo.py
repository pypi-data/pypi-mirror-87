# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Bdo(Component):
    """
    The HTML Bidirectional Text Override element (<bdo>) overrides the current directionality of text, so that the text within is rendered in a different direction.
    """

    def __init__(self, *slots, dir=None):
        super().__init__(*slots)

        self.attr(**{"dir": dir})

    def render(self):
        return Component(tag_name="bdo").proxy(self).render()
