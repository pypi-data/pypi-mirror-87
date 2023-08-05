# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Param(Component):
    def __init__(self, *slots, name=None, value=None):
        self.attr({"name": name, "value": value})

        super().__init__(*slots)

    def render(self):
        return Component(tag_name="param").proxy(self).render()
