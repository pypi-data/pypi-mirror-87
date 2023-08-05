# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Ins(Component):
    """
    The HTML <ins> element represents a range of text that has been added to a document. You can use the <del> element to similarly represent a range of text that has been deleted from the document.
    """

    def __init__(self, *slots, cite=None, datetime=None):
        super().__init__(*slots)

        self.attr(**{"cite": cite, "datetime": datetime})

    def render(self):
        return Component(tag_name="ins").proxy(self).render()
