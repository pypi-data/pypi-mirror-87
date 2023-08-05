# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Area(Component):
    def __init__(self, *slots, alt=None):
        self.attr({"alt": alt})

        super().__init__(*slots)

    def render(self):
        return Component(tag_name="area").proxy(self).render()
