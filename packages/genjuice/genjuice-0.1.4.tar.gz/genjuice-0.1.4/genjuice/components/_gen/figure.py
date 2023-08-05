# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Figure(Component):
    """
    The HTML <figure> (Figure With Optional Caption) element represents self-contained content, potentially with an optional caption, which is specified using the (<figcaption>) element. The figure, its caption, and its contents are referenced as a single unit.
    """

    def __init__(
        self,
        *slots,
    ):
        super().__init__(*slots)

    def render(self):
        return Component(tag_name="figure").proxy(self).render()
