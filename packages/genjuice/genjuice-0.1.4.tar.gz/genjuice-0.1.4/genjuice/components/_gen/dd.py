# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Dd(Component):
    """
    The HTML <dd> element provides the description, definition, or value for the preceding term (<dt>) in a description list (<dl>).
    """

    def __init__(
        self,
        *slots,
    ):
        super().__init__(*slots)

    def render(self):
        return Component(tag_name="dd").proxy(self).render()
