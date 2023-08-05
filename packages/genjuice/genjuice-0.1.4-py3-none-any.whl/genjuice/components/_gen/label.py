# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Label(Component):
    """
    The HTML <label> element represents a caption for an item in a user interface.
    """

    def __init__(self, *slots, for_=None):
        super().__init__(*slots)

        self.attr(**{"for": for_})

    def render(self):
        return Component(tag_name="label").proxy(self).render()
