# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Data(Component):
    """
    The HTML <data> element links a given piece of content with a machine-readable translation. If the content is time- or date-related, the <time> element must be used.
    """

    def __init__(self, *slots, value=None):
        super().__init__(*slots)

        self.attr(**{"value": value})

    def render(self):
        return Component(tag_name="data").proxy(self).render()
