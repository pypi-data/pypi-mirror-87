# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Time(Component):
    """
    The HTML <time> element represents a specific period in time. It may include the datetime attribute to translate dates into machine-readable format, allowing for better search engine results or custom features such as reminders.
    """

    def __init__(self, *slots, datetime=None):
        super().__init__(*slots)

        self.attr(**{"datetime": datetime})

    def render(self):
        return Component(tag_name="time").proxy(self).render()
