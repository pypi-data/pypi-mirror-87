# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Map(Component):
    """
    The HTML <map> element is used with <area> elements to define an image map (a clickable link area).
    """

    def __init__(self, *slots, name=None):
        super().__init__(*slots)

        self.attr(**{"name": name})

    def render(self):
        return Component(tag_name="map").proxy(self).render()
