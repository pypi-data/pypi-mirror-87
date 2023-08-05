# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Caption(Component):
    """
    The HTML <caption> element specifies the caption (or title) of a table.
    """

    def __init__(self, *slots, left=None, top=None, right=None, bottom=None):
        super().__init__(*slots)

        self.attr(**{"left": left, "top": top, "right": right, "bottom": bottom})

    def render(self):
        return Component(tag_name="caption").proxy(self).render()
