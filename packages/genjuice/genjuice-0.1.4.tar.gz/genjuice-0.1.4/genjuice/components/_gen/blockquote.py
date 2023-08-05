# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Blockquote(Component):
    """
    The HTML <blockquote> Element (or HTML Block Quotation Element) indicates that the enclosed text is an extended quotation. Usually, this is rendered visually by indentation (see Notes for how to change it). A URL for the source of the quotation may be given using the cite attribute, while a text representation of the source can be given using the <cite> element.
    """

    def __init__(self, *slots, cite=None):
        super().__init__(*slots)

        self.attr(**{"cite": cite})

    def render(self):
        return Component(tag_name="blockquote").proxy(self).render()
