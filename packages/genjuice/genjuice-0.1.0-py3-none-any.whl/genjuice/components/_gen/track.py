# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Track(Component):
    def __init__(
        self, *slots, default=None, kind=None, label=None, src=None, srclang=None
    ):
        self.attr(
            {
                "default": default,
                "kind": kind,
                "label": label,
                "src": src,
                "srclang": srclang,
            }
        )

        super().__init__(*slots)

    def render(self):
        return Component(tag_name="track").proxy(self).render()
