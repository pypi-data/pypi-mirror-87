# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Blockquote(Component):
    def __init__(self, *slots, cite=None):
        self.attr({"cite": cite})

        super().__init__(*slots)

    def render(self):
        return Component(tag_name="blockquote").proxy(self).render()
