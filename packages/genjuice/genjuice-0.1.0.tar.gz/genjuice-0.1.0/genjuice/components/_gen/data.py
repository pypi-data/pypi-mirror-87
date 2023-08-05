# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Data(Component):
    def __init__(self, *slots, value=None):
        self.attr({"value": value})

        super().__init__(*slots)

    def render(self):
        return Component(tag_name="data").proxy(self).render()
