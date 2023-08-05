# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Dfn(Component):
    """
    The HTML Definition element (<dfn>) is used to indicate the term being defined within the context of a definition phrase or sentence. The <p> element, the <dt>/<dd> pairing, or the <section> element which is the nearest ancestor of the <dfn> is considered to be the definition of the term.
    """

    def __init__(
        self,
        *slots,
    ):
        super().__init__(*slots)

    def render(self):
        return Component(tag_name="dfn").proxy(self).render()
