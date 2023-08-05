# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Slot(Component):
    """
    The HTML <slot> element—part of the Web Components technology suite—is a placeholder inside a web component that you can fill with your own markup, which lets you create separate DOM trees and present them together.
    """

    def __init__(self, *slots, name=None):
        super().__init__(*slots)

        self.attr(**{"name": name})

    def render(self):
        return Component(tag_name="slot").proxy(self).render()
