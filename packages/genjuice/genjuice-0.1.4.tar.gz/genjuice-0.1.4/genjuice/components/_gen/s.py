# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class S(Component):
    """
    The HTML <s> element renders text with a strikethrough, or a line through it. Use the <s> element to represent things that are no longer relevant or no longer accurate. However, <s> is not appropriate when indicating document edits; for that, use the <del> and <ins> elements, as appropriate.
    """

    def __init__(
        self,
        *slots,
    ):
        super().__init__(*slots)

    def render(self):
        return Component(tag_name="s").proxy(self).render()
