# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Em(Component):
    """
    The HTML <em> element marks text that has stress emphasis. The <em> element can be nested, with each level of nesting indicating a greater degree of emphasis.
    """

    def __init__(
        self,
        *slots,
    ):
        super().__init__(*slots)

    def render(self):
        return Component(tag_name="em").proxy(self).render()
