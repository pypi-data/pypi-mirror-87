# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Canvas(Component):
    """
    Use the HTML <canvas> element with either the canvas scripting API or the WebGL API to draw graphics and animations.
    """

    def __init__(self, *slots, height=None, width=None):
        super().__init__(*slots)

        self.attr(**{"height": height, "width": width})

    def render(self):
        return Component(tag_name="canvas").proxy(self).render()
