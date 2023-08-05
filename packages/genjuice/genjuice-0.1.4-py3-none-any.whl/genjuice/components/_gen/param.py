# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Param(Component):
    """
    The HTML <param> element defines parameters for an <object> element.
    """

    def __init__(self, *slots, name=None, value=None):
        super().__init__(*slots)

        self.attr(**{"name": name, "value": value})

    def render(self):
        return Component(tag_name="param").proxy(self).render()
