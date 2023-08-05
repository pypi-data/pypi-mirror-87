# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Var(Component):
    """
    The HTML Variable element (<var>) represents the name of a variable in a mathematical expression or a programming context. It's typically presented using an italicized version of the current typeface, although that behavior is browser-dependent.
    """

    def __init__(
        self,
        *slots,
    ):
        super().__init__(*slots)

    def render(self):
        return Component(tag_name="var").proxy(self).render()
