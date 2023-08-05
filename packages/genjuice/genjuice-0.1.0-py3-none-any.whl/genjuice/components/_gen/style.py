# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Style(Component):
    def __init__(self, *slots, type=None, media=None, nonce=None, title=None):
        self.attr({"type": type, "media": media, "nonce": nonce, "title": title})

        super().__init__(*slots)

    def render(self):
        return Component(tag_name="style").proxy(self).render()
