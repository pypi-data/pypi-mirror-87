# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Output(Component):
    """
    The HTML Output element (<output>) is a container element into which a site or app can inject the results of a calculation or the outcome of a user action.
    """

    def __init__(self, *slots, for_=None, form=None, name=None):
        super().__init__(*slots)

        self.attr(**{"for": for_, "form": form, "name": name})

    def render(self):
        return Component(tag_name="output").proxy(self).render()
