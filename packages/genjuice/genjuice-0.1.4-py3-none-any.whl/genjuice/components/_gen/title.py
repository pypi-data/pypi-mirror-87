# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Title(Component):
    """
    The HTML Title element (<title>) defines the document's title that is shown in a browser's title bar or a page's tab. It only contains text; tags within the element are ignored.
    """

    def __init__(
        self,
        *slots,
    ):
        super().__init__(*slots)

    def render(self):
        return Component(tag_name="title").proxy(self).render()
