# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Del(Component):
    def __init__(self, *slots, cite=None, datetime=None):
        self.attr({"cite": cite, "datetime": datetime})

        super().__init__(*slots)

    def render(self):
        return Component(tag_name="del").proxy(self).render()
