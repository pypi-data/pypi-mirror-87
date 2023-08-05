# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Time(Component):
    def __init__(self, *slots, datetime=None):
        self.attr({"datetime": datetime})

        super().__init__(*slots)

    def render(self):
        return Component(tag_name="time").proxy(self).render()
