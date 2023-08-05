# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Datalist(Component):
    """
    The HTML <datalist> element contains a set of <option> elements that represent the permissible or recommended options available to choose from within other controls.
    """

    def __init__(
        self,
        *slots,
    ):
        super().__init__(*slots)

    def render(self):
        return Component(tag_name="datalist").proxy(self).render()
