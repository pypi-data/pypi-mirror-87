# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Menu(Component):
    """
    This is an experimental technologyCheck the Browser compatibility table carefully before using this in production.
    """

    def __init__(self, *slots, type=None):
        super().__init__(*slots)

        self.attr(**{"type": type})

    def render(self):
        return Component(tag_name="menu").proxy(self).render()
