# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Base(Component):
    """
    The HTML <base> element specifies the base URL to use for all relative URLs in a document. There can be only one <base> element in a document.
    """

    def __init__(self, *slots, href=None, target=None):
        super().__init__(*slots)

        self.attr(**{"href": href, "target": target})

    def render(self):
        return Component(tag_name="base").proxy(self).render()
