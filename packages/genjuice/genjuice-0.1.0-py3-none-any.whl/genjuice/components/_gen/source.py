# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Source(Component):
    def __init__(
        self, *slots, media=None, sizes=None, src=None, srcset=None, type=None
    ):
        self.attr(
            {"media": media, "sizes": sizes, "src": src, "srcset": srcset, "type": type}
        )

        super().__init__(*slots)

    def render(self):
        return Component(tag_name="source").proxy(self).render()
