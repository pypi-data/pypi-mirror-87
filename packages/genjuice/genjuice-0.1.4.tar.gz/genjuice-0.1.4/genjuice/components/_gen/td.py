# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Td(Component):
    """
    The HTML <td> element defines a cell of a table that contains data. It participates in the table model.
    """

    def __init__(self, *slots, colspan=None, headers=None, rowspan=None):
        super().__init__(*slots)

        self.attr(**{"colspan": colspan, "headers": headers, "rowspan": rowspan})

    def render(self):
        return Component(tag_name="td").proxy(self).render()
