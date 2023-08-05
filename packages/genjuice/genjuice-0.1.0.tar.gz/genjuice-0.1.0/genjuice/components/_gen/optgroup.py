# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Optgroup(Component):
    def __init__(self, *slots, disabled=None, label=None):
        self.attr({"disabled": disabled, "label": label})

        super().__init__(*slots)

    def render(self):
        return Component(tag_name="optgroup").proxy(self).render()
