# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Embed(Component):
    """
    The HTML <embed> element embeds external content at the specified point in the document. This content is provided by an external application or other source of interactive content such as a browser plug-in.
    """

    def __init__(self, *slots, height=None, src=None, type=None, width=None):
        super().__init__(*slots)

        self.attr(**{"height": height, "src": src, "type": type, "width": width})

    def render(self):
        return Component(tag_name="embed").proxy(self).render()
