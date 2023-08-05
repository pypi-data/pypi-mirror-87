# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Legend(Component):
    """
    The HTML <legend> element represents a caption for the content of its parent <fieldset>.
    """

    def __init__(
        self,
        *slots,
    ):
        super().__init__(*slots)

    def render(self):
        return Component(tag_name="legend").proxy(self).render()
