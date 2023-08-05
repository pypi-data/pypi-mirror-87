# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Th(Component):
    """
    The HTML <th> element defines a cell as header of a group of table cells. The exact nature of this group is defined by the scope and headers attributes.
    """

    def __init__(
        self, *slots, abbr=None, colspan=None, headers=None, rowspan=None, scope=None
    ):
        super().__init__(*slots)

        self.attr(
            **{
                "abbr": abbr,
                "colspan": colspan,
                "headers": headers,
                "rowspan": rowspan,
                "scope": scope,
            }
        )

    def render(self):
        return Component(tag_name="th").proxy(self).render()
