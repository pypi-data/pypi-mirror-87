# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Ol(Component):
    """
    The HTML <ol> element represents an ordered list of items — typically rendered as a numbered list.
    """

    def __init__(self, *slots, reversed=None, start=None, type=None):
        super().__init__(*slots)

        self.attr(**{"reversed": reversed, "start": start, "type": type})

    def render(self):
        return Component(tag_name="ol").proxy(self).render()
