# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Meter(Component):
    """
    The HTML <meter> element represents either a scalar value within a known range or a fractional value.
    """

    def __init__(
        self,
        *slots,
        value=None,
        min=None,
        max=None,
        low=None,
        high=None,
        optimum=None,
        form=None
    ):
        super().__init__(*slots)

        self.attr(
            **{
                "value": value,
                "min": min,
                "max": max,
                "low": low,
                "high": high,
                "optimum": optimum,
                "form": form,
            }
        )

    def render(self):
        return Component(tag_name="meter").proxy(self).render()
