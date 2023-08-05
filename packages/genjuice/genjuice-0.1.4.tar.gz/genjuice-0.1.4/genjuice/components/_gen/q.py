# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Q(Component):
    """
    The HTML <q> element  indicates that the enclosed text is a short inline quotation. Most modern browsers implement this by surrounding the text in quotation marks. This element is intended for short quotations that don't require paragraph breaks; for long quotations use the <blockquote> element.
    """

    def __init__(self, *slots, cite=None):
        super().__init__(*slots)

        self.attr(**{"cite": cite})

    def render(self):
        return Component(tag_name="q").proxy(self).render()
