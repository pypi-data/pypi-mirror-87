# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Address(Component):
    """
    The HTML <address> element indicates that the enclosed HTML provides contact information for a person or people, or for an organization.
    """

    def __init__(
        self,
        *slots,
    ):
        super().__init__(*slots)

    def render(self):
        return Component(tag_name="address").proxy(self).render()
