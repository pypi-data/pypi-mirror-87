# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Tfoot(Component):
    """
    The HTML <tfoot> element defines a set of rows summarizing the columns of the table.
    """

    def __init__(
        self,
        *slots,
    ):
        super().__init__(*slots)

    def render(self):
        return Component(tag_name="tfoot").proxy(self).render()
