# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Picture(Component):
    """
    The HTML <picture> element contains zero or more <source> elements and one <img> element to offer alternative versions of an image for different display/device scenarios.
    """

    def __init__(
        self,
        *slots,
    ):
        super().__init__(*slots)

    def render(self):
        return Component(tag_name="picture").proxy(self).render()
