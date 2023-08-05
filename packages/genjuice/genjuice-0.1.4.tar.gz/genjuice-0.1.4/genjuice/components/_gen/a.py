# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class A(Component):
    """
    The HTML <a> element (or anchor element), with its href attribute, creates a hyperlink to web pages, files, email addresses, locations in the same page, or anything else a URL can address. Content within each <a> should indicate the link's destination.
    """

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
        super().__init__(*slots)

        self.attr(
            **{
                "download": download,
                "href": href,
                "hreflang": hreflang,
                "ping": ping,
                "rel": rel,
                "target": target,
                "type": type,
            }
        )

    def render(self):
        return Component(tag_name="a").proxy(self).render()
