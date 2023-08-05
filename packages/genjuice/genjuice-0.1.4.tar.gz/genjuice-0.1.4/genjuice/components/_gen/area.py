# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Area(Component):
    """
    The HTML <area> element defines an area inside an image map that has predefined clickable areas. An image map allows geometric areas on an image to be associated with hypertext link.
    """

    def __init__(self, *slots, alt=None):
        super().__init__(*slots)

        self.attr(**{"alt": alt})

    def render(self):
        return Component(tag_name="area").proxy(self).render()
