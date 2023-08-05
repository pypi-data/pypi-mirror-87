# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Option(Component):
    """
    The HTML <option> element is used to define an item contained in a <select>, an <optgroup>, or a <datalist> element. As such, <option> can represent menu items in popups and other lists of items in an HTML document.
    """

    def __init__(self, *slots, disabled=None, label=None, selected=None, value=None):
        super().__init__(*slots)

        self.attr(
            **{
                "disabled": disabled,
                "label": label,
                "selected": selected,
                "value": value,
            }
        )

    def render(self):
        return Component(tag_name="option").proxy(self).render()
