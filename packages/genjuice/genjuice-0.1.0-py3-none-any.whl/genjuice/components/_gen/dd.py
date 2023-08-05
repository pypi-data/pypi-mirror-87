# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Dd(Component):
    def __init__(
        self,
        *slots,
    ):

        super().__init__(*slots)

    def render(self):
        return Component(tag_name="dd").proxy(self).render()
