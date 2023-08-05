# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Col(Component):
    """
    The HTML <col> element defines a column within a table and is used for defining common semantics on all common cells. It is generally found within a <colgroup> element.
    """

    def __init__(self, *slots, span=None):
        super().__init__(*slots)

        self.attr(**{"span": span})

    def render(self):
        return Component(tag_name="col").proxy(self).render()
