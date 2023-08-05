# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Head(Component):
    """
    The HTML <head> element contains machine-readable information (metadata) about the document, like its title, scripts, and style sheets.
    """

    def __init__(
        self,
        *slots,
    ):
        super().__init__(*slots)

    def render(self):
        return Component(tag_name="head").proxy(self).render()
