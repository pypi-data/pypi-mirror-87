# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Form(Component):
    """
    The HTML <form> element represents a document section containing interactive controls for submitting information.
    """

    def __init__(
        self, *slots, accept_charset=None, autocomplete=None, name=None, rel=None
    ):
        super().__init__(*slots)

        self.attr(
            **{
                "accept-charset": accept_charset,
                "autocomplete": autocomplete,
                "name": name,
                "rel": rel,
            }
        )

    def render(self):
        return Component(tag_name="form").proxy(self).render()
