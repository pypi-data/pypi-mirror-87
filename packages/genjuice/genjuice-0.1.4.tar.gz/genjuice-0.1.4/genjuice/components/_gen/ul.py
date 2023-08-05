# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Ul(Component):
    """
    The HTML <ul> element represents an unordered list of items, typically rendered as a bulleted list.
    """

    def __init__(
        self,
        *slots,
    ):
        super().__init__(*slots)

    def render(self):
        return Component(tag_name="ul").proxy(self).render()
