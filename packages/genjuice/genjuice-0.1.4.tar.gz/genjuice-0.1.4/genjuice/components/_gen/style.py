# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Style(Component):
    """
    The HTML <style> element contains style information for a document, or part of a document. It contains CSS, which is applied to the contents of the document containing the <style> element.
    """

    def __init__(self, *slots, type=None, media=None, nonce=None, title=None):
        super().__init__(*slots)

        self.attr(**{"type": type, "media": media, "nonce": nonce, "title": title})

    def render(self):
        return Component(tag_name="style").proxy(self).render()
