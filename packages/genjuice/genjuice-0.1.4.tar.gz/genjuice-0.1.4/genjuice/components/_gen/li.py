# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Li(Component):
    """
    The HTML <li> element is used to represent an item in a list. It must be contained in a parent element: an ordered list (<ol>), an unordered list (<ul>), or a menu (<menu>). In menus and unordered lists, list items are usually displayed using bullet points. In ordered lists, they are usually displayed with an ascending counter on the left, such as a number or letter.
    """

    def __init__(self, *slots, value=None):
        super().__init__(*slots)

        self.attr(**{"value": value})

    def render(self):
        return Component(tag_name="li").proxy(self).render()
