# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Colgroup(Component):
    """
    The HTML <colgroup> element defines a group of columns within a table.
    """

    def __init__(self, *slots, span=None):
        super().__init__(*slots)

        self.attr(**{"span": span})

    def render(self):
        return Component(tag_name="colgroup").proxy(self).render()
