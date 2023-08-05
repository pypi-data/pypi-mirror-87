# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Del(Component):
    """
    The HTML <del> element represents a range of text that has been deleted from a document. This can be used when rendering "track changes" or source code diff information, for example. The <ins> element can be used for the opposite purpose: to indicate text that has been added to the document.
    """

    def __init__(self, *slots, cite=None, datetime=None):
        super().__init__(*slots)

        self.attr(**{"cite": cite, "datetime": datetime})

    def render(self):
        return Component(tag_name="del").proxy(self).render()
