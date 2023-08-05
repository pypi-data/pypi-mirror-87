# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Thead(Component):
    """
    The HTML <thead> element defines a set of rows defining the head of the columns of the table.
    """

    def __init__(
        self,
        *slots,
    ):
        super().__init__(*slots)

    def render(self):
        return Component(tag_name="thead").proxy(self).render()
