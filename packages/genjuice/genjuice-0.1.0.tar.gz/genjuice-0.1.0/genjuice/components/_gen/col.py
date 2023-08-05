# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Col(Component):
    def __init__(self, *slots, span=None):
        self.attr({"span": span})

        super().__init__(*slots)

    def render(self):
        return Component(tag_name="col").proxy(self).render()
