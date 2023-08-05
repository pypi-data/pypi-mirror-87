# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Button(Component):
    """
    The HTML <button> element represents a clickable button, used to submit forms or anywhere in a document for accessible, standard button functionality. By default, HTML buttons are presented in a style resembling the platform the user agent runs on, but you can change buttons’ appearance with CSS.
    """

    def __init__(self, *slots, disabled=None, name=None, type=None, value=None):
        super().__init__(*slots)

        self.attr(**{"disabled": disabled, "name": name, "type": type, "value": value})

    def render(self):
        return Component(tag_name="button").proxy(self).render()
