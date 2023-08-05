# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Form(Component):
    def __init__(
        self, *slots, accept_charset=None, autocomplete=None, name=None, rel=None
    ):
        self.attr(
            {
                "accept-charset": accept_charset,
                "autocomplete": autocomplete,
                "name": name,
                "rel": rel,
            }
        )

        super().__init__(*slots)

    def render(self):
        return Component(tag_name="form").proxy(self).render()
