# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Br(Component):
    """
    The HTML <br> element produces a line break in text (carriage-return). It is useful for writing a poem or an address, where the division of lines is significant.
    """

    def __init__(self, *slots, clear=None):
        super().__init__(*slots)

        self.attr(**{"clear": clear})

    def render(self):
        return Component(tag_name="br").proxy(self).render()
