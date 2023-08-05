# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Html(Component):
    """
    The HTML <html> element represents the root (top-level element) of an HTML document, so it is also referred to as the root element. All other elements must be descendants of this element.
    """

    def __init__(self, *slots, xmlns=None):
        super().__init__(*slots)

        self.attr(**{"xmlns": xmlns})

    def render(self):
        return Component(tag_name="html").proxy(self).render()
