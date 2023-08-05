# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Tr(Component):
    def __init__(
        self, *slots, left=None, center=None, right=None, justify=None, char=None
    ):
        self.attr(
            {
                "left": left,
                "center": center,
                "right": right,
                "justify": justify,
                "char": char,
            }
        )

        super().__init__(*slots)

    def render(self):
        return Component(tag_name="tr").proxy(self).render()
