# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Fieldset(Component):
    """
    The HTML <fieldset> element is used to group several controls as well as labels (<label>) within a web form.
    """

    def __init__(self, *slots, disabled=None, form=None, name=None):
        super().__init__(*slots)

        self.attr(**{"disabled": disabled, "form": form, "name": name})

    def render(self):
        return Component(tag_name="fieldset").proxy(self).render()
