# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Option(Component):
    def __init__(self, *slots, disabled=None, label=None, selected=None, value=None):
        self.attr(
            {"disabled": disabled, "label": label, "selected": selected, "value": value}
        )

        super().__init__(*slots)

    def render(self):
        return Component(tag_name="option").proxy(self).render()
