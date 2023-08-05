# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Output(Component):
    def __init__(self, *slots, for_=None, form=None, name=None):
        self.attr({"for": for_, "form": form, "name": name})

        super().__init__(*slots)

    def render(self):
        return Component(tag_name="output").proxy(self).render()
