# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Html(Component):
    def __init__(self, *slots, xmlns=None):
        self.attr({"xmlns": xmlns})

        super().__init__(*slots)

    def render(self):
        return Component(tag_name="html").proxy(self).render()
