# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Embed(Component):
    def __init__(self, *slots, height=None, src=None, type=None, width=None):
        self.attr({"height": height, "src": src, "type": type, "width": width})

        super().__init__(*slots)

    def render(self):
        return Component(tag_name="embed").proxy(self).render()
