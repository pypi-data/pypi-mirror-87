# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Caption(Component):
    def __init__(self, *slots, left=None, top=None, right=None, bottom=None):
        self.attr({"left": left, "top": top, "right": right, "bottom": bottom})

        super().__init__(*slots)

    def render(self):
        return Component(tag_name="caption").proxy(self).render()
