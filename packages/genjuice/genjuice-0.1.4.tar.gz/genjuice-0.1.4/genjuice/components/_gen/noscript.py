# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Noscript(Component):
    """
    The HTML <noscript> element defines a section of HTML to be inserted if a script type on the page is unsupported or if scripting is currently turned off in the browser.
    """

    def __init__(
        self,
        *slots,
    ):
        super().__init__(*slots)

    def render(self):
        return Component(tag_name="noscript").proxy(self).render()
