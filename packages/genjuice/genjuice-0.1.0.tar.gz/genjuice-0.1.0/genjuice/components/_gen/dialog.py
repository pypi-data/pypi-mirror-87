# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Dialog(Component):
    def __init__(self, *slots, open=None):
        self.attr({"open": open})

        super().__init__(*slots)

    def render(self):
        return Component(tag_name="dialog").proxy(self).render()
