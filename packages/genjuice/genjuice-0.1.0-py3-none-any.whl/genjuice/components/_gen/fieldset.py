# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Fieldset(Component):
    def __init__(self, *slots, disabled=None, form=None, name=None):
        self.attr({"disabled": disabled, "form": form, "name": name})

        super().__init__(*slots)

    def render(self):
        return Component(tag_name="fieldset").proxy(self).render()
