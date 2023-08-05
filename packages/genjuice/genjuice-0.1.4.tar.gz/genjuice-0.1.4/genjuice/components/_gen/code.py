# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Code(Component):
    """
    The HTML <code> element displays its contents styled in a fashion intended to indicate that the text is a short fragment of computer code. By default, the content text is displayed using the user agent's default monospace font.
    """

    def __init__(
        self,
        *slots,
    ):
        super().__init__(*slots)

    def render(self):
        return Component(tag_name="code").proxy(self).render()
