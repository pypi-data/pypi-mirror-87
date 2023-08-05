# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Hgroup(Component):
    """
    The HTML <hgroup> element represents a multi-level heading for a section of a document. It groups a set of <h1>–<h6> elements.
    """

    def __init__(
        self,
        *slots,
    ):
        super().__init__(*slots)

    def render(self):
        return Component(tag_name="hgroup").proxy(self).render()
