# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Button(Component):
    def __init__(self, *slots, disabled=None, name=None, type=None, value=None):
        self.attr({"disabled": disabled, "name": name, "type": type, "value": value})

        super().__init__(*slots)

    def render(self):
        return Component(tag_name="button").proxy(self).render()
