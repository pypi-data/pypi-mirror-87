# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Th(Component):
    def __init__(
        self, *slots, abbr=None, colspan=None, headers=None, rowspan=None, scope=None
    ):
        self.attr(
            {
                "abbr": abbr,
                "colspan": colspan,
                "headers": headers,
                "rowspan": rowspan,
                "scope": scope,
            }
        )

        super().__init__(*slots)

    def render(self):
        return Component(tag_name="th").proxy(self).render()
