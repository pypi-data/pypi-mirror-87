# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Optgroup(Component):
    """
    The HTML <optgroup> element creates a grouping of options within a <select> element.
    """

    def __init__(self, *slots, disabled=None, label=None):
        super().__init__(*slots)

        self.attr(**{"disabled": disabled, "label": label})

    def render(self):
        return Component(tag_name="optgroup").proxy(self).render()
