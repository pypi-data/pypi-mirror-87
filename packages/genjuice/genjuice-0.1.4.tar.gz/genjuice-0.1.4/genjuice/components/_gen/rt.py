# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Rt(Component):
    """
    The HTML Ruby Text (<rt>) element specifies the ruby text component of a ruby annotation, which is used to provide pronunciation, translation, or transliteration information for East Asian typography. The <rt> element must always be contained within a <ruby> element.
    """

    def __init__(
        self,
        *slots,
    ):
        super().__init__(*slots)

    def render(self):
        return Component(tag_name="rt").proxy(self).render()
