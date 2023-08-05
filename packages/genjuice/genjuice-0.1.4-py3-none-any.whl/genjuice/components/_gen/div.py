# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Div(Component):
    """
    The HTML Content Division element (<div>) is the generic container for flow content. It has no effect on the content or layout until styled using CSS.
    """

    def __init__(
        self,
        *slots,
    ):
        super().__init__(*slots)

    def render(self):
        return Component(tag_name="div").proxy(self).render()
