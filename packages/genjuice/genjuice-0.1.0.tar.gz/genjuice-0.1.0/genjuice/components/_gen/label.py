# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Label(Component):
    def __init__(self, *slots, for_=None):
        self.attr({"for": for_})

        super().__init__(*slots)

    def render(self):
        return Component(tag_name="label").proxy(self).render()
