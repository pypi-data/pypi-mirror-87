# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Progress(Component):
    """
    The HTML <progress> element displays an indicator showing the completion progress of a task, typically displayed as a progress bar.
    """

    def __init__(self, *slots, max=None, value=None):
        super().__init__(*slots)

        self.attr(**{"max": max, "value": value})

    def render(self):
        return Component(tag_name="progress").proxy(self).render()
