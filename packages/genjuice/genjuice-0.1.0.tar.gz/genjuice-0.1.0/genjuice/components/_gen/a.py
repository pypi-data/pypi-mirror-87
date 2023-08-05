# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class A(Component):
    def __init__(
        self,
        *slots,
        download=None,
        href=None,
        hreflang=None,
        ping=None,
        rel=None,
        target=None,
        type=None
    ):
        self.attr(
            {
                "download": download,
                "href": href,
                "hreflang": hreflang,
                "ping": ping,
                "rel": rel,
                "target": target,
                "type": type,
            }
        )

        super().__init__(*slots)

    def render(self):
        return Component(tag_name="a").proxy(self).render()
