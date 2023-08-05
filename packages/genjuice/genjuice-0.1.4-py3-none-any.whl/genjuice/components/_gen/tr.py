# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Tr(Component):
    """
    The HTML <tr> element defines a row of cells in a table. The row's cells can then be established using a mix of <td> (data cell) and <th> (header cell) elements.
    """

    def __init__(
        self, *slots, left=None, center=None, right=None, justify=None, char=None
    ):
        super().__init__(*slots)

        self.attr(
            **{
                "left": left,
                "center": center,
                "right": right,
                "justify": justify,
                "char": char,
            }
        )

    def render(self):
        return Component(tag_name="tr").proxy(self).render()
