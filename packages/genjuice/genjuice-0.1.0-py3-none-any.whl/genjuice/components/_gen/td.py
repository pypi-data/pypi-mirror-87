# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Td(Component):
    def __init__(self, *slots, colspan=None, headers=None, rowspan=None):
        self.attr({"colspan": colspan, "headers": headers, "rowspan": rowspan})

        super().__init__(*slots)

    def render(self):
        return Component(tag_name="td").proxy(self).render()
