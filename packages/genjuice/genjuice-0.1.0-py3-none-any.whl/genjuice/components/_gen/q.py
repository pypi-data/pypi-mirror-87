# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Q(Component):
    def __init__(self, *slots, cite=None):
        self.attr({"cite": cite})

        super().__init__(*slots)

    def render(self):
        return Component(tag_name="q").proxy(self).render()
