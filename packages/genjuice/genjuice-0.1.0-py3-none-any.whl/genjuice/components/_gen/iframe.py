# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Iframe(Component):
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
        self.attr(
            {
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

        super().__init__(*slots)

    def render(self):
        return Component(tag_name="iframe").proxy(self).render()
