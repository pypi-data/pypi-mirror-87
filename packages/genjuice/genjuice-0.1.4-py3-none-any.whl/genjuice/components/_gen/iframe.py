# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Iframe(Component):
    """
    The HTML Inline Frame element (<iframe>) represents a nested browsing context, embedding another HTML page into the current one.
    """

    def __init__(
        self,
        *slots,
        allow=None,
        allowfullscreen=None,
        allowpaymentrequest=None,
        height=None,
        name=None,
        referrerpolicy=None,
        sandbox=None,
        src=None,
        srcdoc=None,
        width=None
    ):
        super().__init__(*slots)

        self.attr(
            **{
                "allow": allow,
                "allowfullscreen": allowfullscreen,
                "allowpaymentrequest": allowpaymentrequest,
                "height": height,
                "name": name,
                "referrerpolicy": referrerpolicy,
                "sandbox": sandbox,
                "src": src,
                "srcdoc": srcdoc,
                "width": width,
            }
        )

    def render(self):
        return Component(tag_name="iframe").proxy(self).render()
